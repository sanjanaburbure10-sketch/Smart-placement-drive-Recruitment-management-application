from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json

from .models import User, Job, Application, SavedJob


# ---------- PAGES ----------
def login_page(request):
    return render(request, "login/login.html")

def signup_page(request):
    return render(request, "login/signup.html")

def student_dashboard(request):
    return render(request, "login/student_dashboard.html")

def admin_dashboard(request):
    return render(request, "login/admin_dashboard.html")


# ---------- AUTH ----------
@csrf_exempt
def signup_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        email = data.get("email")

        allowed_admins = [
            "anjaliprakash8867@gmail.com",
            "rahulunki00@gmail.com"
        ]

        role = "admin" if email in allowed_admins else "student"

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        User.objects.create(
            name=data.get("name"),
            email=email,
            password=data.get("password"),
            role=role,
            degree=data.get("degree"),
            cgpa=data.get("cgpa"),
            skills=data.get("skills"),
        )

        return JsonResponse({"message": "Signup successful"})


@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        allowed_admins = [
            "anjaliprakash8867@gmail.com",
            "rahulunki00@gmail.com"
        ]

        try:
            user = User.objects.get(email=email, password=password)

            role = "admin" if email in allowed_admins else "student"

            return JsonResponse({
                "success": True,
                "name": user.name,
                "email": user.email,
                "role": role,
                "user_id": user.id
            })

        except User.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Invalid credentials"
            })


# ---------- JOB ----------
@csrf_exempt
def add_job(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Job.objects.create(
            title=data.get("title"),
            company=data.get("company"),
            location=data.get("location"),
            min_cgpa=data.get("min_cgpa"),
            description=data.get("description"),
        )

        return JsonResponse({"message": "Job added"})


def get_jobs(request):
    jobs = list(Job.objects.values())
    return JsonResponse(jobs, safe=False)


@csrf_exempt
def delete_job(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Job.objects.filter(id=data.get("id")).delete()
        return JsonResponse({"message": "Job deleted"})


# ---------- APPLY ----------
@csrf_exempt
def apply_job(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        job_id = request.POST.get("job_id")
        resume = request.FILES.get("resume")

        Application.objects.create(
            student_id=student_id,
            job_id=job_id,
            resume=resume
        )

        return JsonResponse({"message": "Applied successfully"})


def my_applications(request, user_id):
    apps = Application.objects.filter(student_id=user_id).values(
        "job__title", "status"
    )
    return JsonResponse(list(apps), safe=False)


def all_applications(request):
    apps = Application.objects.select_related('student', 'job')

    data = []
    for a in apps:
        data.append({
            "id": a.id,
            "student_name": a.student.name,
            "student_email": a.student.email,
            "job_title": a.job.title,
            "company": a.job.company,
            "status": a.status,
            "resume": a.resume.url if a.resume else ""
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def update_status(request):
    data = json.loads(request.body)

    app = Application.objects.get(id=data.get("id"))
    app.status = data.get("status")
    app.save()

    return JsonResponse({"message": "Updated"})


# ---------- SAVED JOBS ----------
@csrf_exempt   # ✅ VERY IMPORTANT (fixes your 403 error)
def save_job(request):
    if request.method == "POST":
        data = json.loads(request.body)

        student_id = data.get("student_id")
        job_id = data.get("job_id")

        # ❌ prevent duplicate saves
        if SavedJob.objects.filter(student_id=student_id, job_id=job_id).exists():
            return JsonResponse({"message": "Already saved"})

        SavedJob.objects.create(
            student_id=student_id,
            job_id=job_id
        )

        return JsonResponse({"message": "saved"})


def get_saved_jobs(request, user_id):
    saved = SavedJob.objects.filter(student_id=user_id).select_related("job")

    data = []
    for s in saved:
        data.append({
            "id": s.job.id,   # 👈 IMPORTANT for UI actions
            "title": s.job.title,
            "company": s.job.company,
            "location": s.job.location
        })

    return JsonResponse(data, safe=False)