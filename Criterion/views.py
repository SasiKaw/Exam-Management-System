import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import *
from django.db import transaction


from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def add_criterion(request):
    programs = Programs.objects.all().order_by('name')
    ca_natures = ['In class', 'Quiz']
    fe_natures = ['Essay', 'MCQ']
    
    #Build context dictionary with programs and nature options.
    context = {
        'programs': programs,
        'ca_natures': ca_natures,
        'fe_natures': fe_natures
    }
    
    return render(request, 'criterion/addCriterion.html', context)

def get_batches(request):
    try:
        program_id = request.GET.get('program_id')
        print(f"Received program_id: {program_id}")  # Debug log
        
        if not program_id:
            return JsonResponse({'error': 'Program ID is required'}, status=400)
        
        # Check if program exists
        if not Programs.objects.filter(id=program_id).exists():
            return JsonResponse({'error': f'Program with ID {program_id} not found'}, status=404)
            
        # Query active batches for the given program, ordering them by name.
        batches = Batches.objects.filter(
            programs_id=program_id,
            is_active=True
        ).order_by('name')
        
        # Debug logs
        print(f"SQL Query: {batches.query}")
        print(f"Found {batches.count()} batches")
        batch_list = list(batches.values('id', 'name'))
        print(f"Batch list: {batch_list}")
        
        # Return the batch list as a JSON response.
        return JsonResponse({'batches': batch_list})
        
    except Exception as e:
        import traceback
        print(f"Error in get_batches: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

def get_courses(request):
    try:
        batch_id = request.GET.get('batch_id')
        course_id = request.GET.get('course_id')
        
        if not batch_id and not course_id:
            return JsonResponse({'error': 'Either batch_id or course_id is required'}, status=400)

        base_query = Courses.objects.select_related('subjects')
        
        if course_id:
            # For single course details
            courses = base_query.filter(id=course_id)
        else:
            # For batch course listing
            if not Batches.objects.filter(id=batch_id).exists():
                return JsonResponse({'error': f'Batch with ID {batch_id} not found'}, status=404)
                
            courses = base_query.filter(coursesbatches__batches_id=batch_id, coursesbatches__status=0)

        # Prepare a list of course details to return in the JSON response.
        course_list = courses.values(
            'id',
            'subjects__name',
            'subjects__code',
            'subjects__total_credit',
            'subjects__ca',
            'subjects__fe'
        ).distinct()
            
        return JsonResponse({'courses': list(course_list)})
        
    except Exception as e:
        print(f"Error in get_courses: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def get_last_number(course_id, assessment_type):
    existing_criteria = Criterias.objects.filter(
        courses_id=course_id,
        type=assessment_type
    ).order_by('-name')
    
    last_number = 0
    for criterion in existing_criteria:
        try:
             #Extract digits from the name and convert to an integer
            number = int(''.join(filter(str.isdigit, criterion.name)))
            last_number = max(last_number, number)
        except ValueError:
            continue
    return last_number

def get_next_ca_number(request):
    try:
        course_id = request.GET.get('course_id')
        assessment_type = request.GET.get('type')
        
        # Get the last numeric part from the existing criteria.
        last_number = get_last_number(course_id, assessment_type)
        next_number = last_number + 1
        
        name = f"{assessment_type} {next_number}"
        
        print(f"Last number: {last_number}, Next number: {next_number}")
        return JsonResponse({'name': name, 'last_number': last_number})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    

def get_criteria(request):
    try:
        course_id = request.GET.get('course_id')
        if not course_id:
            return JsonResponse({'error': 'Course ID is required'}, status=400)

        # Retrieve all criteria for the given course. 
        criteria = Criterias.objects.filter(courses_id=course_id)

        # Convert the queryset to a list of dictionaries with selected fields
        criteria_list = list(criteria.values('id', 'name', 'nature', 'type', 'weights'))
        
        return JsonResponse({'criteria': criteria_list})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def save_criteria(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body from the request.
            data = json.loads(request.body)
            course_id = data.get('course_id')
            criteria_type = data.get('type')
            criteria_list = data.get('criteria')

            with transaction.atomic():
                # Get existing criteria IDs for this course and type
                existing_ids = set(Criterias.objects.filter(
                    courses_id=course_id,
                    type=criteria_type
                ).values_list('id', flat=True))
                
                # Process each criterion
                for criterion in criteria_list:
                    if criterion.get('id') in existing_ids:
                        # Update existing
                        Criterias.objects.filter(id=criterion['id']).update(
                            nature=criterion['nature'],
                            weights=criterion['weight']
                        )
                        existing_ids.remove(criterion['id'])
                    else:
                         # If it's a new criterion, create a new record in the database.
                        Criterias.objects.create(
                            courses_id=course_id,
                            nature=criterion['nature'],
                            type=criteria_type,
                            name=criterion['name'],
                            weights=criterion['weight']
                        )
                
                 # Any remaining IDs in existing_ids are criteria that were removed; delete them.
                if existing_ids:
                    Criterias.objects.filter(id__in=existing_ids).delete()
                    
                return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error saving criteria: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})


def ca_schedule_view(request):
    programs = Programs.objects.all().order_by('name')
    
    # Get all CA schedules regardless of course
    events = CaSechedule.objects.select_related(
        'criterias', 
        'criterias__courses', 
        'criterias__courses__subjects'
    ).values(
        'id',
        'start_date',
        'criterias__name',
        'criterias__courses__subjects__name'
    )
    
    calendar_events = [{
        'id': event['id'],
        'title': f"{event['criterias__courses__subjects__name']} - {event['criterias__name']}",
        'start': event['start_date'].isoformat(),
        'allDay': True
    } for event in events]
    
    context = {
        'programs': programs,
        'initial_events': json.dumps(calendar_events)
    }
    
    return render(request, 'criterion/ca_schedule.html', context)

def get_ca_criteria(request):
    try:
        course_id = request.GET.get('course_id')
        criteria = Criterias.objects.filter(
            courses_id=course_id,
            type='CA'  # Only get CA criteria
        ).values('id', 'name', 'nature')
        return JsonResponse({'criteria': list(criteria)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def save_ca_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            criteria_id = data.get('criteria_id')
            start_date = data.get('start_date')
            
            schedule = CaSechedule.objects.create(
                criterias_id=criteria_id,
                start_date=start_date
            )
            
            return JsonResponse({'status': 'success', 'id': schedule.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def get_ca_events(request):
    try:
        course_id = request.GET.get('course_id')
        events = CaSechedule.objects.select_related(
            'criterias', 
            'criterias__courses', 
            'criterias__courses__subjects'
        ).filter(
            criterias__courses_id=course_id
        ).values(
            'id',
            'start_date',
            'criterias__name',
            'criterias__courses__subjects__name'
        )
        
        calendar_events = [{
            'id': event['id'],
            'title': f"{event['criterias__courses__subjects__name']} - {event['criterias__name']}",
            'start': event['start_date'].isoformat(),
            'allDay': True
        } for event in events]
        
        return JsonResponse({'events': calendar_events})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)