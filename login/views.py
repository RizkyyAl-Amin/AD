from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, PasswordResetForm, OTPForm
from .models import CustomUser, OTP
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
import random


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('list_produk') 
        else:
            messages.error(request, 'Email atau password salah!')

    return render(request, 'pages/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def password_reset_view(request):
    email = None
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '').strip()
            user = CustomUser.objects.filter(email=email).first()
            if user:
                otp_code = OTP.generate_otp()
                OTP.objects.create(user=user, otp_code=otp_code)
                try:
                    send_mail(
                        'Reset Password OTP',
                        f'Kode OTP Anda adalah {otp_code}. Berlaku selama 5 menit.',
                        'noreply@example.com',
                        [email],
                    )
                    messages.success(request, 'Kode OTP telah dikirim ke email Anda.')
                    return redirect(f'/otp-verify/?email={email}')
                except Exception as e:
                    messages.error(request, 'Gagal mengirim email. Coba lagi nanti.')
            else:
                messages.error(request, 'Email tidak terdaftar.')
    else:
        form = PasswordResetForm()
    return render(request, 'pages/password_reset.html', {'form': form, 'email': email})

def otp_verify_view(request):
    email = request.GET.get('email')  
    if not email:  
        messages.error(request, 'Email harus diisi.')
        return redirect('password_reset')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data.get('otp_code')  
            otp = OTP.objects.filter(
                otp_code=otp_code,
                user__email=email,
                is_used=False,
                created_at__gte=now() - timedelta(minutes=5)
            ).first()
            if otp:
                otp.is_used = True  
                otp.save()
                messages.success(request, 'Kode OTP valid. Silakan masukkan password baru.')
                 
                return redirect(f'/new-password/?email={email}')  
            else:
                messages.error(request, 'Kode OTP tidak valid atau sudah kedaluwarsa.')
        else:
            messages.error(request, 'Form tidak valid. Harap isi semua field dengan benar.')
    else:
        form = OTPForm()

    
    return render(request, 'pages/otp_verify.html', {'form': form, 'email': email})



def resend_otp_view(request):
    email = request.GET.get('email')
    if not email:
        messages.error(request, 'Email harus diisi.')
        return redirect('password_reset')

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        messages.error(request, 'Email tidak ditemukan.')
        return redirect('password_reset')

    OTP.objects.filter(user=user, is_used=False).delete()
    new_otp = OTP.objects.create(
        user=user,
        otp_code=random.randint(100000, 999999),
    )
    send_mail(
        'Kode OTP Reset Kata Sandi',
        f'Kode OTP Anda adalah: {new_otp.otp_code}',
        'no-reply@alindiesel.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, 'Kode OTP telah dikirim ulang ke email Anda.')
    return redirect(f'/otp-verify/?email={email}')


def new_password_view(request):
    email = request.GET.get('email')
    if not email:
        messages.error(request, 'Email harus diisi.')
        return redirect('password_reset')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Password tidak cocok. Silakan coba lagi.')
            return redirect(f'/new-password/?email={email}')

        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password berhasil diubah. Silakan login.')
            return redirect('login')
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan coba lagi.')

    return render(request, 'pages/new_password.html', {'email': email})
