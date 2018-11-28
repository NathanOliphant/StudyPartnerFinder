from django.shortcuts import render
from studygroups.models import Course, Subject, CurrentSemester
from django.shortcuts import redirect
from .forms import SearchForm
from studygroups.utils import GetStudygroupsForCourse


# from django.contrib import messages
#
#    The courses.SearchTemplate class provides a searchbox and search functionality
#     for courses.  As a class, it can be easily imported into other views and templates.
#
class SearchTemplate(object):
    form = SearchForm()  # An unbound form
    # Courses returned should be all active, and for the current semester.
    # These values, added to context, are so we can work with course and subject
    # objects in the template beyond just the searchbox.
    current_semester = CurrentSemester.objects.get()
    subject_results = Subject.objects.all()
    courses_results = Course.objects.filter(
        is_active = 1,
        semester = current_semester.semester,
        year = current_semester.year
    )

    # Since we are using a class, we do not need to use return render(),
    # just need to include a context and form, and this class will later be
    # used for other views.
    context = {
        'subject_list': subject_results,
        'course_list': courses_results,
        'form': form,
        'current_semester': current_semester
    }


# Create your views here.
#
#    index is our default courses view.  It uses the SearchTemplate class as a basis
#    for its context.
#
def index(request, course_id = None):
    # We use the same form regardless of POST or GET, so add or None
    # so that we have an unbound form for first load.
    form = SearchForm(request.POST or None)
    # If the form has been submitted, it will be a POST, and we need to validate the data.
    if request.method == 'POST':
        # All validation rules pass
        if form.is_valid():
            # Process the data in form.cleaned_data
            data = form.cleaned_data

            selected_course = data['study_courses']

            # We should have a specific course now, so redirect to the course details page.
            context = { 'course_id': selected_course }
            return redirect('/courses/{}'.format(selected_course))
        else:
            # This would mean some validation rule did not pass.
            # We should do something here if that is the case.
            # Or, just ignore and let it drop into loading the search interface again.
            pass
    else:
        # If we are here, either the POST went horribly wrong, or this was a get request.
        # So, load our SearchTemplate class as the context, and go to the index page
        # so that our user can search.
        context = SearchTemplate.context

        return render(request, 'courses/index.html', context)


#
#    course view displays the course details, including associated studygroups.
#
def course(request, course_id = None):
    # If no id passed in, we need to redirect to the search page.
    if course_id is None:
        return redirect('/search/')

    # Need to keep track of all studygroups for this course, so put them here.
    course_studygroups = GetStudygroupsForCourse(request.user, course_id)
    # We should only have one course, so grab the first active course that matches our id.
    #
    course_results = Course.objects.filter(is_active = 1, id = course_id).first()
    # We should probably check that course_results returned a valid result, and if not,
    # redirect back to search.  That will be in the next iteration.

    context = { 'course': course_results, 'studygroup_list': course_studygroups }
    return render(request, 'courses/course.html', context)
