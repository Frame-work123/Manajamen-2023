from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import ijinkan_pengguna, tolakhalaman_ini, pilihan_login
from django.conf import settings
# 
from django.db.models import Sum, Q, Count, Avg, F, Max, Subquery, OuterRef, Func, Window
from statistics import mean,median,stdev
from django.db.models.functions import Rank, DenseRank
from django.db.models.expressions import Func

from time import gmtime, strftime

def index(request):
	context = {
	'page_title':'Login Managemen SMK',
	}
	#print(request.user)
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('Home')
		else:
			return redirect('index')

	return render(request, 'login.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def HomeView(request):	
	context = {
	'page_title':'Aplikasi Manajemen Akademik & (PPDB)'
	}
	group_admin = Group.objects.get(name="Admin")
	group_user = Group.objects.get(name="User")
	admin_group = request.user.groups.all()

	template_name = None
	if group_admin in admin_group:
		template_name = 'index.html'
	elif group_user in admin_group:
		template_name = 'halaman_ppdb.html'
	else:
		template_name = 'index.html'

	return render(request, template_name,  context)

def LogoutView(request):
	context = {
	'page_title':'logout',
	}
	if request.method == "POST":
		if request.POST["logout"] == "Submit":	
			logout(request)

		return redirect('index')

	return render(request, 'logout.html',  context)	

# ----------data kelas----------
@login_required(login_url=settings.LOGIN_URL)
def Data_kelas(request):
	data_kelas = Model_kelas.objects.all()
	context = {	

	'data_kelas': data_kelas,
	}
	return render(request, 'Master_data/data_kelas/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_kelas(request):
	if request.method == 'POST':
		Model_kelas.objects.create(
			nama_kelas = request.POST['nama_kelas'],
			kapasitas = request.POST['kapasitas'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Kelas/")	
	context = {	
	'Tambah siswa': 'Tambah siswa'
	}
	return render(request, 'Master_data/data_kelas/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_kelas(request, id_kls):		
	edit_kelas = Model_kelas.objects.get(id=id_kls)
	if request.method == 'POST':
			edit_kelas.nama_kelas = request.POST.get('nama_kelas')			
			edit_kelas.kapasitas = request.POST.get('kapasitas')
			edit_kelas.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Kelas')

	context = {'edit_kelas': edit_kelas}
	return render(request, 'Master_data/data_kelas/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_kelas(request, id_kls):
	Model_kelas.objects.filter(id=id_kls).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Kelas')

# ----------data siswa----------
@login_required(login_url=settings.LOGIN_URL)
def Data_siswa(request):
	data_siswa = Model_siswa.objects.all()
	context = {	
	'data_siswa': data_siswa,
	}
	return render(request, 'Master_data/data_siswa/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_siswa(request):
	select_kelas = Model_kelas.objects.all()
	select_jurusan = Model_jurusan.objects.all()
	if request.method == 'POST':
		Model_siswa.objects.create(
			nis = request.POST['nis'],
			nama_lengkap = request.POST['nama_lengkap'],
			jk = request.POST['jk'],			
			alamat = request.POST['alamat'],
			tempat_lahir = request.POST['tempat_lahir'],
			tanggal_lahir = request.POST['tanggal_lahir'],
			nohp = request.POST['nohp'],
			jurusan = request.POST['jurusan'],
			kelas = request.POST['kelas'],			
			foto = request.FILES['foto'],			
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Siswa/")	
	context = {	
	'Tambah siswa': 'Tambah siswa',
	'select_kelas': select_kelas,
	'select_jurusan': select_jurusan
	}
	return render(request, 'Master_data/data_siswa/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_siswa(request, id_siswa):
	select_kelas = Model_kelas.objects.all()
	select_jurusan = Model_jurusan.objects.all()
	edit_siswa = Model_siswa.objects.get(id=id_siswa)
	if request.method == 'POST':		
			edit_siswa.nis = request.POST.get('nis')
			edit_siswa.nama_lengkap = request.POST.get('nama_lengkap')			
			edit_siswa.jk = request.POST.get('jk')						
			edit_siswa.alamat = request.POST.get('alamat')
			edit_siswa.tempat_lahir = request.POST.get('tempat_lahir')
			edit_siswa.tanggal_lahir = request.POST.get('tanggal_lahir')
			edit_siswa.nohp = request.POST.get('nohp')
			edit_siswa.jurusan = request.POST.get('jurusan')
			edit_siswa.kelas = request.POST.get('kelas')
			edit_siswa.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Siswa')

	context = {
	'edit_siswa': edit_siswa,
	'select_kelas': select_kelas,
	'select_jurusan': select_jurusan
	}
	return render(request, 'Master_data/data_siswa/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_foto_siswa(request, id_siswa):
	edit_siswa = Model_siswa.objects.get(id=id_siswa)
	if request.method == 'POST':		
			edit_siswa.foto = request.FILES.get('foto')
			edit_siswa.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Siswa')

	context = {
	'edit_siswa': edit_siswa,
	}
	return render(request, 'Master_data/data_siswa/edit_foto.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_siswa(request, id_siswa):
	Model_siswa.objects.filter(id=id_siswa).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Siswa')

# ----------data mata pelajaran----------
@login_required(login_url=settings.LOGIN_URL)
def Data_mapel(request):
	data_kelompok = Model_matapelajaran.objects.values('kelompok_mapel').distinct()
	

	kelompok_A = Model_matapelajaran.objects.all()
	context = {	
	'data_kelompok': data_kelompok,
	'kelompok_A': kelompok_A,
	
	}
	return render(request, 'Master_data/data_mapel/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_mapel(request):
	if request.method == 'POST':
		Model_matapelajaran.objects.create(
			kode_mapel = request.POST['kode_mapel'],
			nama_mapel = request.POST['nama_mapel'],
			keterangan = request.POST['keterangan'],
			kelompok_mapel = request.POST['kelompok_mapel'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Mapel/")	
	context = {	
	'Tambah': 'Tambah'
	}
	return render(request, 'Master_data/data_mapel/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_mapel(request, id_mapel):		
	edit_mapel = Model_matapelajaran.objects.get(id=id_mapel)
	if request.method == 'POST':
			edit_mapel.kode_mapel = request.POST.get('kode_mapel')			
			edit_mapel.nama_mapel = request.POST.get('nama_mapel')
			edit_mapel.keterangan = request.POST.get('keterangan')
			edit_mapel.kelompok_mapel = request.POST.get('kelompok_mapel')
			edit_mapel.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Mapel')

	context = {'edit_mapel': edit_mapel}
	return render(request, 'Master_data/data_mapel/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_mapel(request, id_mapel):
	Model_matapelajaran.objects.filter(id=id_mapel).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Mapel')

# ----------data mata guru----------
@login_required(login_url=settings.LOGIN_URL)
def Data_guru(request):
	data_guru = Model_guru.objects.all()
	context = {	

	'data_guru': data_guru,
	}
	return render(request, 'Master_data/data_guru/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_guru(request):
	if request.method == 'POST':
		Model_guru.objects.create(
			nidn = request.POST['nidn'],
			nama = request.POST['nama'],
			alamat = request.POST['alamat'],
			tempat_lahir = request.POST['tempat_lahir'],
			jk = request.POST['jk'],
			nohp = request.POST['nohp'],
			jabatan = request.POST['jabatan'],
			foto = request.FILES['foto'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Guru/")	
	context = {	
	'Tambah': 'Tambah'
	}
	return render(request, 'Master_data/data_guru/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_guru(request, id_guru):		
	edit_guru = Model_guru.objects.get(id=id_guru)
	if request.method == 'POST':
			edit_guru.nidn = request.POST.get('nidn')			
			edit_guru.nama = request.POST.get('nama')
			edit_guru.alamat = request.POST.get('alamat')
			edit_guru.tempat_lahir = request.POST.get('tempat_lahir')
			edit_guru.jk = request.POST.get('jk')
			edit_guru.nohp = request.POST.get('nohp')
			edit_guru.jabatan = request.POST.get('jabatan')
			edit_guru.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Guru')

	context = {'edit_guru': edit_guru}
	return render(request, 'Master_data/data_guru/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_foto_guru(request, id_guru):
	edit_guru = Model_guru.objects.get(id=id_guru)
	if request.method == 'POST':		
			edit_guru.foto = request.FILES.get('foto')
			edit_guru.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Guru')

	context = {
	'edit_guru': edit_guru,
	}
	return render(request, 'Master_data/data_guru/edit_foto.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_guru(request, id_guru):
	Model_guru.objects.filter(id=id_guru).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Guru')

# ----------data mata Jurusan----------
@login_required(login_url=settings.LOGIN_URL)
def Data_jurusan(request):
	data_jurusan = Model_jurusan.objects.all()
	context = {	

	'data_jurusan': data_jurusan,
	}
	return render(request, 'Master_data/data_jurusan/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_jurusan(request):
	if request.method == 'POST':
		Model_jurusan.objects.create(
			nama_jurusan = request.POST['nama_jurusan'],
			keterangan = request.POST['keterangan'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Jurusan/")	
	context = {	
	'Tambah': 'Tambah'
	}
	return render(request, 'Master_data/data_jurusan/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_jurusan(request, id_jurusan):		
	edit_jurusan = Model_jurusan.objects.get(id=id_jurusan)
	if request.method == 'POST':
			edit_jurusan.nama_jurusan = request.POST.get('nama_jurusan')			
			edit_jurusan.keterangan = request.POST.get('keterangan')
			edit_jurusan.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Jurusan')

	context = {'edit_jurusan': edit_jurusan}
	return render(request, 'Master_data/data_jurusan/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_jurusan(request, id_jurusan):
	Model_jurusan.objects.filter(id=id_jurusan).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Jurusan')

# ----------data mata jadwal----------
@login_required(login_url=settings.LOGIN_URL)
def Data_jadwal(request):
	data_jadwal = Model_jadwall.objects.all()
	context = {	

	'data_jadwal': data_jadwal,
	}
	return render(request, 'Master_data/data_jadwal/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_jadwal(request):
	data_guru = Model_guru.objects.all()
	data_jurusan = Model_jurusan.objects.all()
	data_mapel = Model_matapelajaran.objects.all()
	data_kelas = Model_kelas.objects.all()
	# cari data mapel
	if 'cari_mapel' in request.GET:
		cari_mapel=request.GET['cari_mapel']
		tampil_mapel = Model_matapelajaran.objects.filter(nama_mapel=cari_mapel)
	else:
		tampil_mapel = Model_matapelajaran.objects.filter(nama_mapel=None)				

	if request.method == 'POST':
		Model_jadwall.objects.create(
			nama_jadwal = request.POST['nama_jadwal'],
			tanggal_jadwal = request.POST['tanggal_jadwal'],
			hari = request.POST['hari'],
			nama_mapel = request.POST['nama_mapel'],
			kode_guru = request.POST['kode_guru'],
			nama_guru = request.POST['nama_guru'],
			jurusan = request.POST['jurusan'],
			kelas = request.POST['kelas'],
			jam_mapel = request.POST['jam_mapel'],
			jam_masuk = request.POST['jam_masuk'],
			jam_istirahat = request.POST['jam_istirahat'],
			keterangan = request.POST['keterangan'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Jadwal/")	
	context = {	
	'Tambah': 'Tambah',
	'data_guru': data_guru,
	'data_jurusan': data_jurusan,
	'data_mapel': data_mapel,
	'data_kelas': data_kelas,
	'tampil_mapel': tampil_mapel,
	}
	return render(request, 'Master_data/data_jadwal/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_jadwal(request, id_jadwal):		
	data_guru = Model_guru.objects.all()
	data_jurusan = Model_jurusan.objects.all()
	data_mapel = Model_matapelajaran.objects.all()
	data_kelas = Model_kelas.objects.all()
	edit_jadwal = Model_jadwall.objects.get(id=id_jadwal)
	if request.method == 'POST':
			edit_jadwal.nama_jadwal = request.POST.get('nama_jadwal')			
			edit_jadwal.tanggal_jadwal = request.POST.get('tanggal_jadwal')
			edit_jadwal.hari = request.POST.get('hari')
			edit_jadwal.nama_mapel = request.POST.get('nama_mapel')
			edit_jadwal.kode_guru = request.POST.get('kode_guru')
			edit_jadwal.nama_guru = request.POST.get('nama_guru')
			edit_jadwal.jurusan = request.POST.get('jurusan')
			edit_jadwal.kelas = request.POST.get('kelas')
			edit_jadwal.jam_mapel = request.POST.get('jam_mapel')
			edit_jadwal.jam_masuk = request.POST.get('jam_masuk')
			edit_jadwal.jam_istirahat = request.POST.get('jam_istirahat')
			edit_jadwal.keterangan = request.POST.get('keterangan')
			edit_jadwal.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Jadwal')

	context = {
	'data_guru': data_guru,
	'data_jurusan': data_jurusan,
	'data_mapel': data_mapel,
	'data_kelas': data_kelas,
	'edit_jadwal': edit_jadwal
	}
	return render(request, 'Master_data/data_jadwal/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_jadwal(request, id_jadwal):
	Model_jadwall.objects.filter(id=id_jadwal).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Jadwal')

def View_jadwal(request):
	data_jadwal = Model_jadwall.objects.values('hari').distinct()	
	# atur jam mapel sabtu
	tampil_sabtu1 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu2 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu3 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu4 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu5 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel minggu
	tampil_minggu1 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu2 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu3 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu4 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu5 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Senin
	tampil_senin1 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin2 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin3 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin4 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin5 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Selasa
	tampil_selasa1 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa2 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa3 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa4 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa5 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Rabu
	tampil_rabu1 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu2 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu3 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu4 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu5 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Kamis
	tampil_kamis1 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis2 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis3 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis4 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis5 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Jumat
	tampil_jumat1 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat2 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat3 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat4 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat5 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()

	# data sabtu
	tampil_sabtu_X = Model_jadwall.objects.filter(hari='Sabtu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_sabtu_XI = Model_jadwall.objects.filter(hari='Sabtu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_sabtu_XII = Model_jadwall.objects.filter(hari='Sabtu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# data minggu
	tampil_minggu_X = Model_jadwall.objects.filter(hari='Minggu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_minggu_XI = Model_jadwall.objects.filter(hari='Minggu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_minggu_XII = Model_jadwall.objects.filter(hari='Minggu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# data senin
	tampil_senin_X = Model_jadwall.objects.filter(hari='Senin', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_senin_XI = Model_jadwall.objects.filter(hari='Senin', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_senin_XII = Model_jadwall.objects.filter(hari='Senin', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# data selasa
	tampil_selasa_X = Model_jadwall.objects.filter(hari='Selasa', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_selasa_XI = Model_jadwall.objects.filter(hari='Selasa', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_selasa_XII = Model_jadwall.objects.filter(hari='Selasa', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# rabu
	tampil_rabu_X = Model_jadwall.objects.filter(hari='Rabu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_rabu_XI = Model_jadwall.objects.filter(hari='Rabu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_rabu_XII = Model_jadwall.objects.filter(hari='Rabu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# kamis
	tampil_kamis_X = Model_jadwall.objects.filter(hari='Kamis', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_kamis_XI = Model_jadwall.objects.filter(hari='Kamis', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_kamis_XII = Model_jadwall.objects.filter(hari='Kamis', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# juma'at
	tampil_jumat_X = Model_jadwall.objects.filter(hari='Jumat', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_jumat_XI = Model_jadwall.objects.filter(hari='Jumat', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_jumat_XII = Model_jadwall.objects.filter(hari='Jumat', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	

	context = {
	'data_jadwal': data_jadwal,
	# atur jam mapel sabtu
	'tampil_sabtu1': tampil_sabtu1,
	'tampil_sabtu2': tampil_sabtu2,
	'tampil_sabtu3': tampil_sabtu3,
	'tampil_sabtu4': tampil_sabtu4,
	'tampil_sabtu5': tampil_sabtu5,
	# atur jam mapel Minggu
	'tampil_minggu1': tampil_minggu1,
	'tampil_minggu2': tampil_minggu2,
	'tampil_minggu3': tampil_minggu3,
	'tampil_minggu4': tampil_minggu4,
	'tampil_minggu5': tampil_minggu5,
	# atur jam mapel Senin
	'tampil_senin1': tampil_senin1,
	'tampil_senin2': tampil_senin2,
	'tampil_senin3': tampil_senin3,
	'tampil_senin4': tampil_senin4,
	'tampil_senin5': tampil_senin5,
	# atur jam mapel Selasa
	'tampil_selasa1': tampil_selasa1,
	'tampil_selasa2': tampil_selasa2,
	'tampil_selasa3': tampil_selasa3,
	'tampil_selasa4': tampil_selasa4,
	'tampil_selasa5': tampil_selasa5,
	# atur jam mapel Rabu
	'tampil_rabu1': tampil_rabu1,
	'tampil_rabu2': tampil_rabu2,
	'tampil_rabu3': tampil_rabu3,
	'tampil_rabu4': tampil_rabu4,
	'tampil_rabu5': tampil_rabu5,
	# atur jam mapel Kamis
	'tampil_kamis1': tampil_kamis1,
	'tampil_kamis2': tampil_kamis2,
	'tampil_kamis3': tampil_kamis3,
	'tampil_kamis4': tampil_kamis4,
	'tampil_kamis5': tampil_kamis5,
	# atur jam mapel Jumat
	'tampil_jumat1': tampil_jumat1,
	'tampil_jumat2': tampil_jumat2,
	'tampil_jumat3': tampil_jumat3,
	'tampil_jumat4': tampil_jumat4,
	'tampil_jumat5': tampil_jumat5,
	# sabtu
	'tampil_sabtu_X': tampil_sabtu_X,
	'tampil_sabtu_XI': tampil_sabtu_XI,
	'tampil_sabtu_XII': tampil_sabtu_XII,
	# minggu
	'tampil_minggu_X': tampil_minggu_X,
	'tampil_minggu_XI': tampil_minggu_XI,
	'tampil_minggu_XII': tampil_minggu_XII,
	# senin
	'tampil_senin_X': tampil_senin_X,
	'tampil_senin_XI': tampil_senin_XI,
	'tampil_senin_XII': tampil_senin_XII,
	# selasa
	'tampil_selasa_X': tampil_selasa_X,
	'tampil_selasa_XI': tampil_selasa_XI,
	'tampil_selasa_XII': tampil_selasa_XII,
	# rabu
	'tampil_rabu_X': tampil_rabu_X,
	'tampil_rabu_XI': tampil_rabu_XI,
	'tampil_rabu_XII': tampil_rabu_XII,
	# kamis
	'tampil_kamis_X': tampil_kamis_X,
	'tampil_kamis_XI': tampil_kamis_XI,
	'tampil_kamis_XII': tampil_kamis_XII,
	# jumat
	'tampil_jumat_X': tampil_jumat_X,
	'tampil_jumat_XI': tampil_jumat_XI,
	'tampil_jumat_XII': tampil_jumat_XII,
	}
	return render(request, 'Master_data/data_jadwal/view_jadwal.html',  context)

def Laporan_jadwal(request):
	data_jadwal = Model_jadwall.objects.values('hari').distinct()	
	# atur jam mapel sabtu
	tampil_sabtu1 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu2 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu3 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu4 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_sabtu5 = Model_jadwall.objects.filter(hari='Sabtu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel minggu
	tampil_minggu1 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu2 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu3 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu4 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_minggu5 = Model_jadwall.objects.filter(hari='Minggu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Senin
	tampil_senin1 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin2 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin3 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin4 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_senin5 = Model_jadwall.objects.filter(hari='Senin', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Selasa
	tampil_selasa1 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa2 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa3 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa4 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_selasa5 = Model_jadwall.objects.filter(hari='Selasa', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Rabu
	tampil_rabu1 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu2 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu3 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu4 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_rabu5 = Model_jadwall.objects.filter(hari='Rabu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Kamis
	tampil_kamis1 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis2 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis3 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis4 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_kamis5 = Model_jadwall.objects.filter(hari='Kamis', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	# atur jam mapel Jumat
	tampil_jumat1 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat2 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat3 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat4 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	tampil_jumat5 = Model_jadwall.objects.filter(hari='Jumat', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()

	# data sabtu
	tampil_sabtu_X = Model_jadwall.objects.filter(hari='Sabtu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_sabtu_XI = Model_jadwall.objects.filter(hari='Sabtu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_sabtu_XII = Model_jadwall.objects.filter(hari='Sabtu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# data minggu
	tampil_minggu_X = Model_jadwall.objects.filter(hari='Minggu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_minggu_XI = Model_jadwall.objects.filter(hari='Minggu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_minggu_XII = Model_jadwall.objects.filter(hari='Minggu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# data senin
	tampil_senin_X = Model_jadwall.objects.filter(hari='Senin', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_senin_XI = Model_jadwall.objects.filter(hari='Senin', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_senin_XII = Model_jadwall.objects.filter(hari='Senin', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# data selasa
	tampil_selasa_X = Model_jadwall.objects.filter(hari='Selasa', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_selasa_XI = Model_jadwall.objects.filter(hari='Selasa', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_selasa_XII = Model_jadwall.objects.filter(hari='Selasa', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# rabu
	tampil_rabu_X = Model_jadwall.objects.filter(hari='Rabu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_rabu_XI = Model_jadwall.objects.filter(hari='Rabu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_rabu_XII = Model_jadwall.objects.filter(hari='Rabu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# kamis
	tampil_kamis_X = Model_jadwall.objects.filter(hari='Kamis', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_kamis_XI = Model_jadwall.objects.filter(hari='Kamis', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_kamis_XII = Model_jadwall.objects.filter(hari='Kamis', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	# juma'at
	tampil_jumat_X = Model_jadwall.objects.filter(hari='Jumat', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_jumat_XI = Model_jadwall.objects.filter(hari='Jumat', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	tampil_jumat_XII = Model_jadwall.objects.filter(hari='Jumat', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	

	context = {
	'data_jadwal': data_jadwal,
	# atur jam mapel sabtu
	'tampil_sabtu1': tampil_sabtu1,
	'tampil_sabtu2': tampil_sabtu2,
	'tampil_sabtu3': tampil_sabtu3,
	'tampil_sabtu4': tampil_sabtu4,
	'tampil_sabtu5': tampil_sabtu5,
	# atur jam mapel Minggu
	'tampil_minggu1': tampil_minggu1,
	'tampil_minggu2': tampil_minggu2,
	'tampil_minggu3': tampil_minggu3,
	'tampil_minggu4': tampil_minggu4,
	'tampil_minggu5': tampil_minggu5,
	# atur jam mapel Senin
	'tampil_senin1': tampil_senin1,
	'tampil_senin2': tampil_senin2,
	'tampil_senin3': tampil_senin3,
	'tampil_senin4': tampil_senin4,
	'tampil_senin5': tampil_senin5,
	# atur jam mapel Selasa
	'tampil_selasa1': tampil_selasa1,
	'tampil_selasa2': tampil_selasa2,
	'tampil_selasa3': tampil_selasa3,
	'tampil_selasa4': tampil_selasa4,
	'tampil_selasa5': tampil_selasa5,
	# atur jam mapel Rabu
	'tampil_rabu1': tampil_rabu1,
	'tampil_rabu2': tampil_rabu2,
	'tampil_rabu3': tampil_rabu3,
	'tampil_rabu4': tampil_rabu4,
	'tampil_rabu5': tampil_rabu5,
	# atur jam mapel Kamis
	'tampil_kamis1': tampil_kamis1,
	'tampil_kamis2': tampil_kamis2,
	'tampil_kamis3': tampil_kamis3,
	'tampil_kamis4': tampil_kamis4,
	'tampil_kamis5': tampil_kamis5,
	# atur jam mapel Jumat
	'tampil_jumat1': tampil_jumat1,
	'tampil_jumat2': tampil_jumat2,
	'tampil_jumat3': tampil_jumat3,
	'tampil_jumat4': tampil_jumat4,
	'tampil_jumat5': tampil_jumat5,
	# sabtu
	'tampil_sabtu_X': tampil_sabtu_X,
	'tampil_sabtu_XI': tampil_sabtu_XI,
	'tampil_sabtu_XII': tampil_sabtu_XII,
	# minggu
	'tampil_minggu_X': tampil_minggu_X,
	'tampil_minggu_XI': tampil_minggu_XI,
	'tampil_minggu_XII': tampil_minggu_XII,
	# senin
	'tampil_senin_X': tampil_senin_X,
	'tampil_senin_XI': tampil_senin_XI,
	'tampil_senin_XII': tampil_senin_XII,
	# selasa
	'tampil_selasa_X': tampil_selasa_X,
	'tampil_selasa_XI': tampil_selasa_XI,
	'tampil_selasa_XII': tampil_selasa_XII,
	# rabu
	'tampil_rabu_X': tampil_rabu_X,
	'tampil_rabu_XI': tampil_rabu_XI,
	'tampil_rabu_XII': tampil_rabu_XII,
	# kamis
	'tampil_kamis_X': tampil_kamis_X,
	'tampil_kamis_XI': tampil_kamis_XI,
	'tampil_kamis_XII': tampil_kamis_XII,
	# jumat
	'tampil_jumat_X': tampil_jumat_X,
	'tampil_jumat_XI': tampil_jumat_XI,
	'tampil_jumat_XII': tampil_jumat_XII,
	}
	return render(request, 'Master_data/data_jadwal/lp_jadwal.html',  context)

# nilai raport
@login_required(login_url=settings.LOGIN_URL)
def Data_nilai_raport(request):
	# mengelompokkan
	data_kelompok = Model_nilairapot.objects.values('nama_siswa','no_induk','nama_jurusan').distinct()
	# kelompok mapel
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	data_mapel = Model_matapelajaran.objects.all()

	data_nilai_raport = Model_nilairapot.objects.all()
	context = {	
	'data_kelompok': data_kelompok,
	'kelompok_mapel': kelompok_mapel,
	'data_mapel': data_mapel,
	'data_nilai_raport': data_nilai_raport,
	}
	return render(request, 'Master_data/data_nilai_raport/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_nilai_raport(request):
	select_mapel = Model_matapelajaran.objects.all()
	# cari siswa
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_siswa = Model_siswa.objects.filter(nis=cari_data)
	else:
		tampil_siswa = Model_siswa.objects.filter(nis=None)

	# proses kelompok mapel
	data_kelompok = Model_matapelajaran.objects.values('kelompok_mapel').distinct()
	kelompok_A = Model_matapelajaran.objects.all()
	if request.method == 'POST':
		Model_nilairapot.objects.create(
			nama_siswa = request.POST['nama_siswa'],
			no_induk = request.POST['no_induk'],
			nama_kelas = request.POST['nama_kelas'],
			nama_jurusan = request.POST['nama_jurusan'],
			nama_mapel = request.POST['nama_mapel'],
			kelompok_mapel = request.POST['kelompok_mapel'],
			nilai_pengetahuan = request.POST['nilai_pengetahuan'],
			deskripsi_pengetahuan = request.POST['deskripsi_pengetahuan'],
			nilai_keterampilan = request.POST['nilai_keterampilan'],
			deskripsi_keterampilan = request.POST['deskripsi_keterampilan'],
			nilai_kkm = request.POST['nilai_kkm'],
			jumlah_nilai = request.POST['jumlah_nilai'],
			rata_rata = request.POST['rata_rata'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Nilai/")	
	context = {	
	'Tambah siswa': 'Tambah siswa',
	'tampil_siswa': tampil_siswa,
	'select_mapel': select_mapel,
	'data_kelompok': data_kelompok,
	'kelompok_A': kelompok_A,
	}
	return render(request, 'Master_data/data_nilai_raport/tambah.html', context)


@login_required(login_url=settings.LOGIN_URL)
def Edit_nilai_raport(request, id_nilai):
	# proses kelompok mapel
	data_kelompok = Model_matapelajaran.objects.values('kelompok_mapel').distinct()
	kelompok_A = Model_matapelajaran.objects.all()

	select_mapel = Model_matapelajaran.objects.all()
	edit_nilai_r = Model_nilairapot.objects.get(id=id_nilai)
	if request.method == 'POST':
			edit_nilai_r.nama_siswa = request.POST.get('nama_siswa')			
			edit_nilai_r.no_induk = request.POST.get('no_induk')
			edit_nilai_r.nama_kelas = request.POST.get('nama_kelas')
			edit_nilai_r.nama_jurusan = request.POST.get('nama_jurusan')
			edit_nilai_r.nama_mapel = request.POST.get('nama_mapel')
			edit_nilai_r.kelompok_mapel = request.POST.get('kelompok_mapel')
			edit_nilai_r.nilai_pengetahuan = request.POST.get('nilai_pengetahuan')
			edit_nilai_r.deskripsi_pengetahuan = request.POST.get('deskripsi_pengetahuan')
			edit_nilai_r.nilai_keterampilan = request.POST.get('nilai_keterampilan')
			edit_nilai_r.deskripsi_keterampilan = request.POST.get('deskripsi_keterampilan')
			edit_nilai_r.nilai_kkm = request.POST.get('nilai_kkm')
			edit_nilai_r.jumlah_nilai = request.POST.get('jumlah_nilai')
			edit_nilai_r.rata_rata = request.POST.get('rata_rata')
			edit_nilai_r.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Nilai')

	context = {
	'edit_nilai_r': edit_nilai_r,
	'select_mapel': select_mapel,

	'data_kelompok': data_kelompok,
	'kelompok_A': kelompok_A,
	}
	return render(request, 'Master_data/data_nilai_raport/edit.html',  context)

tampil_siswa = Model_siswa.objects.filter(nis=None)
@login_required(login_url=settings.LOGIN_URL)
def Edit_keterangan_raport(request, id_nilai):		
	edit_nilai_r = Model_nilairapot.objects.get(id=id_nilai)
	if request.method == 'POST':
		# tambah ekstra kurikuler
			edit_nilai_r.kegiatan_ekstra = request.POST.get('kegiatan_ekstra')			
			edit_nilai_r.keterangan_esktra = request.POST.get('keterangan_esktra')
		# prestasi
			edit_nilai_r.prestasi = request.POST.get('prestasi')
			edit_nilai_r.keterangan_prestasi = request.POST.get('keterangan_prestasi')
		# ketidak hadiran
			edit_nilai_r.jml_sakit = request.POST.get('jml_sakit')
			edit_nilai_r.jml_izin = request.POST.get('jml_izin')
			edit_nilai_r.tanpa_keterangan = request.POST.get('tanpa_keterangan')
		# keputusan
			edit_nilai_r.keterangan_raport = request.POST.get('keterangan_raport')
			edit_nilai_r.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Nilai')

	context = {
	'edit_nilai_r': edit_nilai_r,
	}
	return render(request, 'Master_data/data_nilai_raport/edit_keterangan.html',  context)	

@login_required(login_url=settings.LOGIN_URL)
def Hapus_nilai_raport(request, id_nilai):
	Model_nilairapot.objects.filter(id=id_nilai).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Nilai')

# raport
@login_required(login_url=settings.LOGIN_URL)
def Data_raport(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data).values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
	else:
		data_raport = Model_nilairapot.objects.filter(no_induk=None)

	# hitung nilai pengetahuan	
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		Nilai_pengetahuan = Model_nilairapot.objects.filter(no_induk=cari_data).aggregate(Jumlah=Sum('nilai_pengetahuan'))
	else:
		Nilai_pengetahuan = Model_nilairapot.objects.filter(no_induk=None)

	

	# hitung nilai keterampilan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		Nilai_keterampilan = Model_nilairapot.objects.filter(no_induk=cari_data).aggregate(Jumlah=Sum('nilai_keterampilan'))
	else:
		Nilai_keterampilan = Model_nilairapot.objects.filter(no_induk=None)


	# hitung nilai rata-rata pengetahuan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		# N_rata = Model_nilairapot.objects.filter(no_induk=cari_data).count()
		N_rata_P = Model_nilairapot.objects.aggregate(N_pengetahuan=Count('nilai_pengetahuan', filter=Q(no_induk=cari_data)))
		
	else:
		N_rata_P = Model_nilairapot.objects.filter(no_induk=None)

	# hitung nilai rata-rata keterampilan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		N_rata_K = Model_nilairapot.objects.aggregate(N_keterampilan=Count('nilai_keterampilan', filter=Q(no_induk=cari_data)))
		
	else:
		N_rata_K = Model_nilairapot.objects.filter(no_induk=None)

	# tanggal sekarang
    
	

	

	# proses kelas X
	# proses nilai raport cari kelompok A Wajib
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='A', nama_kelas='X').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=None)


	# proses nilai raport cari kelompok B Wajib
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='B', nama_kelas='X').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok C Peminatan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='C', nama_kelas='X').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok Mulok
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='Mulok', nama_kelas='X').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=None)

	# perbandingan nilai siswa-siswi
	
	# kelas X
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='X', jurusan="Rekayasa Perangkat Lunak (RPL)")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)



	# cari nilai
	# if 'cari_data' in request.GET:
	# 	cari_data=request.GET['cari_data']
	# 	nilai_rap = Model_peringkat.objects.filter(no_induk=cari_data,kelas='X', jurusan="Rekayasa Perangkat Lunak (RPL)")
	
	# for np in nilai_rap:
	# 	nil = np.nilai_raport
	

	data_rap = Model_peringkat.objects.filter(kelas='X', jurusan="Rekayasa Perangkat Lunak (RPL)").aggregate(max=Max('nilai_raport'))
	# data_rap = Model_peringkat.objects.filter(kelas='X', jurusan="Rekayasa Perangkat Lunak (RPL)").order_by('-nilai_raport')
	
	# proses ulang
	
	# aa = Model_peringkat.objects.filter(no_induk=cari_data).annotate(rank=Window(expression=Rank(), order_by=F('nilai_raport').desc()))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Rekayasa Perangkat Lunak (RPL)").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Rekayasa Perangkat Lunak (RPL)").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Rekayasa Perangkat Lunak (RPL)").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
	else:
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=None)	
	
	# kepala sekolah raport
	kepala_sekolah = Model_guru.objects.filter(jabatan='Kepala Sekolah')
    

    

	context = {	
	'data_raport': data_raport,
	'kelompok_mapel': kelompok_mapel,

	# nilai raport cari
	'tampil_kelompok': tampil_kelompok,
	'tampil_kelompok_B': tampil_kelompok_B,
	'tampil_kelompok_C': tampil_kelompok_C,
	'tampil_kelompok_mulok': tampil_kelompok_mulok,
	# hitung nilai pengetahuan dan keterampilan
	'Nilai_pengetahuan': Nilai_pengetahuan,
	'Nilai_keterampilan': Nilai_keterampilan,
	# hitung nilai rata2 pengetahuan dan keterampilan
	'N_rata_P': N_rata_P,
	'N_rata_K': N_rata_K,
	# chek prediksi
	'chek_relasi': chek_relasi,
	# 'nil': nil,
	'data_rap': data_rap,

	# perbandingan nilai atau peringkat

	# kriteria
	'kriteria': kriteria,
	'prestasi': prestasi,
	'ketidak_hadiran': ketidak_hadiran,

	'tanggal_sekarang': tanggal_sekarang,
	# kepala sekolah
	'kepala_sekolah': kepala_sekolah,
	
	}
	return render(request, 'Master_data/data_nilai_raport/detail.html',  context)

# halaman menu laporan
@login_required(login_url=settings.LOGIN_URL)
def Menu_laporan_admin(request):
	data_kelas = Model_kelas.objects.all()
	select_jurusan = Model_jurusan.objects.all()
	context = {	
	'select_jurusan': select_jurusan,
	'data_kelas': data_kelas,
	}
	return render(request, 'Master_data/laporan/menu.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_siswa(request):
	
	if 'cari_jurusan' in request.GET:
		cari_jurusan=request.GET['cari_jurusan']
		cari_kelas=request.GET['cari_kelas']
		lpsiswa = Model_siswa.objects.filter(jurusan=cari_jurusan, kelas=cari_kelas)
	else:
		lpsiswa = Model_siswa.objects.filter(id=None)

	context = {		
	'lpsiswa': lpsiswa,

	}
	return render(request, 'Master_data/laporan/lp_siswa.html',  context)