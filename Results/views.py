import json
from django.forms import FloatField
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.db.models import F, FloatField, Sum, ExpressionWrapper
import numpy as np
from scipy import stats

def result_view(request):
    programs = Programs.objects.all()
    course_id = request.GET.get('course')
    batch_id = request.GET.get('batch')
    mode = request.GET.get('mode')
    
    
    context = {
        'programs': programs,
        'is_update': mode == 'update',
        'selected_course': course_id,
        'selected_batch': batch_id
    }
    
    if mode == 'update' and course_id and batch_id:
        try:
            course = Courses.objects.select_related('subjects__programs', 'subjects', 'semesters').get(id=course_id)
            context.update({
                'selected_program': course.subjects.programs.id,
                'selected_batch': batch_id,
                'selected_course': course_id,
                'course_name': f"{course.subjects.name} ({course.semesters.start_date.strftime('%Y-%m-%d')})"  # Add this line
            })
        except Courses.DoesNotExist:
            messages.error(request, "Course not found")
            return redirect('Results:finalize_dashboard') 
    
    if request.method == 'POST':
        try:
            student_results = request.POST.getlist('grades[]')
            student_ids = request.POST.getlist('student_ids[]')
            course_id = request.POST.get('course_id')
            batch_id = request.POST.get('batch_id')
            
            # Update results
            for student_id, grade in zip(student_ids, student_results):
                Results.objects.update_or_create(
                    students_id=student_id,
                    courses_id=course_id,
                    defaults={'grade': grade}  # Save to grade field instead of s_grade
                )
            
            # Update course status
            CoursesBatches.objects.filter(
                courses_id=course_id,
                batches_id=batch_id
            ).update(status=1)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'BOE/results.html', context)

def get_batches(request):
    program_id = request.GET.get('program_id')
    batches = Batches.objects.filter(programs_id=program_id, is_active=1)
    return JsonResponse({
        'batches': list(batches.values('id', 'name'))
    })

def get_courses(request):
    batch_id = request.GET.get('batch_id')
    courses = Courses.objects.filter(
        coursesbatches__batches_id=batch_id,
        coursesbatches__status=0
    ).select_related('subjects', 'semesters')
    
    return JsonResponse({
        'courses': [{
            'id': course.id,
            'name': f"{course.subjects.name} ({course.semesters.start_date.strftime('%Y-%m-%d')})"
        } for course in courses]
    })

def get_students(request):
    batch_id = request.GET.get('batch_id')
    course_id = request.GET.get('course_id')
    
    # Get course details including subject
    course = Courses.objects.select_related('subjects').get(id=course_id)
    
    students = Students.objects.filter(batches_id=batch_id)

    # Get all criteria for this course
    criteria = Criterias.objects.filter(courses_id=course_id)
    ca_criteria = criteria.filter(type='CA')
    fe_criteria = criteria.filter(type='FE')
    
    
    # Calculate total CA and FE contributions
    ca_contribution = course.subjects.ca  
    fe_contribution = course.subjects.fe  
    
    student_marks = []
    for student in students:
        # Calculate CA marks
        ca_total = 0
        ca_details = []
        for ca in ca_criteria:
            try:
                mark = StudentsCriterias.objects.get(
                    students_id=student.id,
                    criterias_id=ca.id
                )
                raw_mark = float(mark.mark)
                weighted_mark = (raw_mark / 100) * ca.weights
                contribution_mark = (weighted_mark / 100) * ca_contribution
                ca_total += contribution_mark
                ca_details.append({
                    'name': ca.name,
                    'raw_mark': raw_mark,
                    'weighted_mark': weighted_mark,
                    'contribution_mark': contribution_mark
                })
            except StudentsCriterias.DoesNotExist:
                continue
        
        # Calculate FE marks
        fe_total = 0
        fe_details = []
        for fe in fe_criteria:
            try:
                mark = StudentsCriterias.objects.get(
                    students_id=student.id,
                    criterias_id=fe.id
                )
                raw_mark = float(mark.mark)
                weighted_mark = (raw_mark / 100) * fe.weights
                contribution_mark = (weighted_mark / 100) * fe_contribution
                fe_total += contribution_mark
                fe_details.append({
                    'name': fe.name,
                    'raw_mark': raw_mark,
                    'weighted_mark': weighted_mark,
                    'contribution_mark': contribution_mark
                })
            except StudentsCriterias.DoesNotExist:
                continue
        
        # Get course mark and grades
        try:
            course_mark = CoursesStudent.objects.get(
                students_id=student.id,
                courses_id=course_id
            ).marks
        except CoursesStudent.DoesNotExist:
            course_mark = 0
            
        try:
            result = Results.objects.get(
                students_id=student.id,
                courses_id=course_id
            )
            system_grade = result.s_grade
            approved_grade = result.grade
        except Results.DoesNotExist:
            system_grade = ''
            approved_grade = ''
            
        student_marks.append({
            'id': student.id,
            'name': student.name,
            'ca_total': round(ca_total, 2),
            'ca_details': ca_details,
            'fe_total': round(fe_total, 2),
            'fe_details': fe_details,
            'course_mark': course_mark,
            'system_grade': system_grade,
            'approved_grade': approved_grade,
        })

        response_data = {
        'ca_contrib':ca_contribution,
        'fe_contrib':fe_contribution,
        'students': student_marks,
    }
    
    return JsonResponse(response_data)
    
    # views.py
def finalize_dashboard(request):
    programs = Programs.objects.all()
    context = {
        'programs': programs
    }
    return render(request, 'BOE/finalize_dashboard.html', context)

def add_criterion_marks(request):
    programs = Programs.objects.all()
    context = {
        'programs': programs
    }
    return render(request, 'BOE/criterion_result.html', context)

def get_batch_courses(request):
    batch_id = request.GET.get('batch_id')
    courses = Courses.objects.filter(
        coursesbatches__batches_id=batch_id,
        coursesbatches__status=1  # Only get courses with status 1
    ).select_related('subjects', 'semesters')
    
    return JsonResponse({
        'courses': [{
            'id': course.id,
            'name': f"{course.subjects.name} ({course.semesters.start_date.strftime('%Y-%m-%d')})"
        } for course in courses]
    })

def update_course_status(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        batch_id = request.POST.get('batch_id')
        
        try:
            course_batch = CoursesBatches.objects.get(
                courses_id=course_id,
                batches_id=batch_id
            )
            course_batch.status = 1
            course_batch.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def get_criteria(request):
    course_id = request.GET.get('course_id')
    criteria = Criterias.objects.filter(courses_id=course_id)
    return JsonResponse({
        'criteria': list(criteria.values('id', 'nature', 'weights', 'type'))
    })

def get_students_marks(request):
    batch_id = request.GET.get('batch_id')
    criterion_id = request.GET.get('criterion_id')
    
    # Get criterion weight for conversion
    criterion = Criterias.objects.get(id=criterion_id)
    
    students = Students.objects.filter(batches_id=batch_id)
    marks = StudentsCriterias.objects.filter(
        criterias_id=criterion_id
    ).values('students_id', 'mark')
    
    # Convert weighted marks back to raw marks for display
    marks_dict = {
        m['students_id']: round(float(m['mark']), 2) 
        for m in marks
    }
    
    return JsonResponse({
        'students': [{
            'id': student.id,
            'name': student.name,
            'current_mark': marks_dict.get(student.id, '')
        } for student in students]
    })


def calculate_grade(mark):
    """
    Calculate grade based on LNBTT grading system
    Args:
        mark: Numerical mark (0-100)
    Returns:
        tuple: (grade, grade_point)
    """
    # Handle special cases first
    if mark is None or mark == '':
        return 'NE', 0  # Not completed the Final Examination

    mark = float(mark)
    
    if mark == 0:
        return 'AE', 0  # Absent for Final Examination

    # Regular grade ranges
    if 85 <= mark <= 100:
        return 'A+'
    elif 70 <= mark <= 84:
        return 'A'
    elif 65 <= mark <= 69:
        return 'A-'
    elif 60 <= mark <= 64:
        return 'B+'
    elif 55 <= mark <= 59:
        return 'B'
    elif 50 <= mark <= 54:
        return 'B-'
    elif 45 <= mark <= 49:
        return 'C+'
    elif 40 <= mark <= 44:
        return 'C'
    elif 35 <= mark <= 39:
        return 'C-'
    elif 30 <= mark <= 34:
        return 'D+'
    elif 25 <= mark <= 29:
        return 'D'
    elif 0 <= mark <= 24:
        return 'E'
    
    return 'E'  # Default case

def determine_attempt_status(ca_marks, fe_marks):
    """
    Determine special grade statuses based on CA and FE completion
    """
    if not ca_marks and not fe_marks:
        return 'AA'  # Absent for both CA and Final
    elif not ca_marks:
        return 'AC'  # Absent for CA
    elif not fe_marks:
        return 'AE'  # Absent for Final Exam
    elif not ca_marks and fe_marks and float(fe_marks) < 40:
        return 'AF'  # Absent for CA and failed final
    return None


def save_criterion_marks(request):
    if request.method == 'POST':
        try:
            criterion_id = request.POST.get('criterion_id')
            student_ids = json.loads(request.POST.get('student_ids'))
            marks = json.loads(request.POST.get('marks'))
            
             # Get criterion details
            criterion = Criterias.objects.get(id=criterion_id)

            # Save marks for each student
            for student_id, percentage_mark in zip(student_ids, marks):

                # Save weighted mark to StudentsCriterias table
                if 0 <= float(percentage_mark) <= 100:
                    StudentsCriterias.objects.update_or_create(
                        students_id=student_id,
                        criterias_id=criterion_id,
                        defaults={'mark': percentage_mark} # Save as percentage mark
                    )

                # Get course ID for further calculations
                course_id = criterion.courses_id
                course = Courses.objects.select_related('subjects').get(id=course_id)

                criteria = Criterias.objects.filter(courses_id=course_id)
                ca_criteria = criteria.filter(type='CA')
                fe_criteria = criteria.filter(type='FE')

                # Calculate total CA and FE contributions
                ca_contribution = course.subjects.ca  
                fe_contribution = course.subjects.fe  

                ca_total = 0
                ca_details = []

                # Calculate CA marks
                for ca in ca_criteria:
                    try:
                        mark = StudentsCriterias.objects.get(
                            students_id=student_id,
                           criterias_id=ca.id
                        )
                        raw_mark = float(mark.mark)
                        weighted_mark = (raw_mark / 100) * ca.weights
                        contribution_mark = (weighted_mark / 100) * ca_contribution
                        ca_total += contribution_mark
                        ca_details.append({
                            'name': ca.name,
                            'raw_mark': raw_mark,
                            'weighted_mark': weighted_mark,
                            'contribution_mark': contribution_mark
                        })
                    except StudentsCriterias.DoesNotExist:
                        continue

                # Calculate FE marks
                fe_total = 0
                fe_details = []
                for fe in fe_criteria:
                    try:
                        mark = StudentsCriterias.objects.get(
                            students_id=student_id,
                            criterias_id=fe.id
                        )
                        raw_mark = float(mark.mark)
                        weighted_mark = (raw_mark / 100) * fe.weights
                        contribution_mark = (weighted_mark / 100) * fe_contribution
                        fe_total += contribution_mark
                        fe_details.append({
                            'name': fe.name,
                            'raw_mark': raw_mark,
                            'weighted_mark': weighted_mark,
                            'contribution_mark': contribution_mark
                        })
                    except StudentsCriterias.DoesNotExist:
                        continue
                    

                final_mark = fe_total + ca_total

                ca_marks = StudentsCriterias.objects.filter(
                    students_id=student_id,
                    criterias__courses_id=course_id,
                    criterias__type='CA'
                ).values_list('mark', flat=True)

                fe_marks = StudentsCriterias.objects.filter(
                    students_id=student_id,
                    criterias__courses_id=course_id,
                    criterias__type='FE'
                ).values_list('mark', flat=True)

                # Determine special statuses first
                attempt_status = determine_attempt_status(ca_marks, fe_marks)
                if attempt_status:
                    grade = attempt_status
                else:
                    grade = calculate_grade(final_mark)

           
                # Update course enrollment record
                CoursesStudent.objects.update_or_create(
                    students_id=student_id,
                    courses_id=course_id,
                    defaults={
                        'marks': final_mark,
                        'status': 1 if not attempt_status else 0
                    }
                )

                # Update results record
                Results.objects.update_or_create(
                    students_id=student_id,
                    courses_id=course_id,
                    defaults={
                        's_grade': grade,
                    }
                )

            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            print(f"Error saving marks: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_grade_summary(request):
    course_id = request.GET.get('course_id')
    batch_id = request.GET.get('batch_id')

    # Get results for the selected course and batch
    results = Results.objects.filter(
        courses_id=course_id,
        students__batches_id=batch_id
    )

    total_results = results.count()
    
    # Include all possible grades
    grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'E', 
              'NC', 'NE', 'AC', 'AE', 'AA', 'AF']
    
    # Get current selections from dropdowns
    current_selections = {}
    for result in results:
        # If grade is set, use it; otherwise use s_grade
        current_selections[result.students_id] = result.grade if result.grade else result.s_grade

    grade_stats = []
    for grade in grades:
        # Count occurrences of this grade in current selections
        count = sum(1 for grade_value in current_selections.values() if grade_value == grade)
        percentage = (count / total_results * 100) if total_results > 0 else 0
        
        grade_stats.append({
            'grade': grade,
            'count': count,
            'percentage': round(percentage, 1)
        })

    return JsonResponse({
        'status': 'success',
        'grade_stats': grade_stats,
        'total_results': total_results
    })






        

        

    