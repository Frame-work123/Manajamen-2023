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
# 
from django.contrib.humanize.templatetags.humanize import intcomma

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
    	# grafiks
	all_ppdb = Model_pendaftaran_pesertaPPDB.objects.all().count()
	all_kelas1 = Model_siswa1.objects.filter(kelas='X').count()
	all_kelas2 = Model_siswa1.objects.filter(kelas='XI').count()
	all_kelas3 = Model_siswa1.objects.filter(kelas='XII').count()
	context = {
	'page_title':'Aplikasi Manajemen Akademik & (PPDB)',
	'all_ppdb': all_ppdb,
	'all_kelas1': all_kelas1,
	'all_kelas2': all_kelas2,
	'all_kelas3': all_kelas3,
	}
	group_admin = Group.objects.get(name="Admin")
	group_user = Group.objects.get(name="User")
	group_pembayaran = Group.objects.get(name="Pembayaran")
	admin_group = request.user.groups.all()

	template_name = None
	if group_admin in admin_group:
		template_name = 'index.html'
	elif group_user in admin_group:
		template_name = 'Master_ppdb/halaman_ppdb.html'
	elif group_pembayaran in admin_group:
		template_name = 'Master_pembayaran/halaman_pembayaran.html'
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

# tahun ajaran
@login_required(login_url=settings.LOGIN_URL)
def Data_tahun(request):
	data_tahun = Model_tahun_pelajaran.objects.all()
	context = {	

	'data_tahun': data_tahun,
	}
	return render(request, 'Master_data/data_tahun/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_tahun(request):
	if request.method == 'POST':
		Model_tahun_pelajaran.objects.create(
			tahun = request.POST['tahun'],
			semester = request.POST['semester'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Tahun/")	
	context = {	
	'Tambah siswa': 'Tambah'
	}
	return render(request, 'Master_data/data_tahun/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_tahun(request, id):		
	edit_tahun = Model_tahun_pelajaran.objects.get(id=id)
	if request.method == 'POST':
			edit_tahun.tahun = request.POST.get('tahun')			
			edit_tahun.semester = request.POST.get('semester')
			edit_tahun.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Tahun')

	context = {'edit_tahun': edit_tahun}
	return render(request, 'Master_data/data_tahun/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_tahun(request, id):
	Model_tahun_pelajaran.objects.filter(id=id).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Tahun')

# ----------data siswa----------
@login_required(login_url=settings.LOGIN_URL)
def Data_siswa(request):
	select_kelas = Model_kelas.objects.all()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_siswa = Model_siswa1.objects.filter(kelas=cari_data)
	elif 'cari_tahun' in request.GET:
		cari_tahun=request.GET['cari_tahun']
		data_siswa = Model_siswa1.objects.filter(tahun_masuk=cari_tahun)
	else:
		data_siswa = Model_siswa1.objects.all()	

	context = {	
	'data_siswa': data_siswa,
	'select_kelas': select_kelas,
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
			tahun_masuk = request.POST['tahun_masuk'],			
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
	edit_siswa = Model_siswa1.objects.get(id=id_siswa)
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
			edit_siswa.tahun_masuk = request.POST.get('tahun_masuk')
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
	edit_siswa = Model_siswa1.objects.get(id=id_siswa)
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
	Model_siswa1.objects.filter(id=id_siswa).delete()
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
	data_tahun = Model_tahun_pelajaran.objects.all()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_jadwal = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data)
	else:
		data_jadwal = Model_jadwall1.objects.all()
	context = {	
	'data_tahun': data_tahun,
	'data_jadwal': data_jadwal,
	}
	return render(request, 'Master_data/data_jadwal/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_jadwal(request):
	data_tahun = Model_tahun_pelajaran.objects.all()
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
		Model_jadwall1.objects.create(
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
			keterangan_jadwal = request.POST['keterangan_jadwal'],
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
	'data_tahun': data_tahun
	}
	return render(request, 'Master_data/data_jadwal/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_jadwal(request, id_jadwal):		
	data_tahun = Model_tahun_pelajaran.objects.all()
	data_guru = Model_guru.objects.all()
	data_jurusan = Model_jurusan.objects.all()
	data_mapel = Model_matapelajaran.objects.all()
	data_kelas = Model_kelas.objects.all()
	edit_jadwal = Model_jadwall1.objects.get(id=id_jadwal)
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
			edit_jadwal.keterangan_jadwal = request.POST.get('keterangan_jadwal')
			edit_jadwal.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Jadwal')

	context = {
	'data_guru': data_guru,
	'data_jurusan': data_jurusan,
	'data_mapel': data_mapel,
	'data_kelas': data_kelas,
	'edit_jadwal': edit_jadwal,
	'data_tahun': data_tahun
	}
	return render(request, 'Master_data/data_jadwal/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_jadwal(request, id_jadwal):
	Model_jadwall1.objects.filter(id=id_jadwal).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Jadwal')

def View_jadwal(request):
	data_jadwal = Model_jadwall1.objects.values('hari').distinct()	
	# atur jam mapel sabtu
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel sabtu
		tampil_sabtu1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel minggu
		tampil_minggu1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Senin
		tampil_senin1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Selasa
		tampil_selasa1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Rabu
		tampil_rabu1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Kamis
		tampil_kamis1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Jumat
		tampil_jumat1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data sabtu
		tampil_sabtu_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_sabtu_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_sabtu_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data minggu
		tampil_minggu_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_minggu_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_minggu_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data senin
		tampil_senin_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_senin_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_senin_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data selasa
		tampil_selasa_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_selasa_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_selasa_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# rabu
		tampil_rabu_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_rabu_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_rabu_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# kamis
		tampil_kamis_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_kamis_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_kamis_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# juma'at
		tampil_jumat_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_jumat_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_jumat_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	

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
	'cari_data': cari_data
	}
	return render(request, 'Master_data/data_jadwal/view_jadwal.html',  context)

def Laporan_jadwal(request):
	data_jadwal = Model_jadwall1.objects.values('hari').distinct()	
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel sabtu
		tampil_sabtu1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_sabtu5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel minggu
		tampil_minggu1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_minggu5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Senin
		tampil_senin1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_senin5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Selasa
		tampil_selasa1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_selasa5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Rabu
		tampil_rabu1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_rabu5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Kamis
		tampil_kamis1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_kamis5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# atur jam mapel Jumat
		tampil_jumat1 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-1').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat2 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-2').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat3 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-3').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat4 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-4').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
		tampil_jumat5 = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', jam_mapel='Ke-5').values('jam_mapel','jam_masuk','jam_istirahat').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data sabtu
		tampil_sabtu_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_sabtu_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_sabtu_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Sabtu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data minggu
		tampil_minggu_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_minggu_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_minggu_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Minggu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data senin
		tampil_senin_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_senin_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_senin_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Senin', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# data selasa
		tampil_selasa_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_selasa_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_selasa_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Selasa', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# rabu
		tampil_rabu_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_rabu_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_rabu_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Rabu', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# kamis
		tampil_kamis_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_kamis_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_kamis_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Kamis', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
	# juma'at
		tampil_jumat_X = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', kelas='X').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_jumat_XI = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', kelas='XI').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
		tampil_jumat_XII = Model_jadwall1.objects.filter(keterangan_jadwal=cari_data,hari='Jumat', kelas='XII').values('jam_mapel','nama_guru','kode_guru','nama_mapel').distinct()
	

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
		tampil_siswa = Model_siswa1.objects.filter(nis=cari_data)
	else:
		tampil_siswa = Model_siswa1.objects.filter(nis=None)

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

tampil_siswa = Model_siswa1.objects.filter(nis=None)
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

# raport kelas X
@login_required(login_url=settings.LOGIN_URL)
def Data_raport(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X').values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
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
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='X', jurusan="Tata Boga")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)


	data_rap = Model_peringkat.objects.filter(kelas='X', jurusan="Tata Boga").aggregate(max=Max('nilai_raport'))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Tata Boga").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Tata Boga").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Tata Boga").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
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
	# kriteria
	'kriteria': kriteria,
	'prestasi': prestasi,
	'ketidak_hadiran': ketidak_hadiran,
	'tanggal_sekarang': tanggal_sekarang,
	# kepala sekolah
	'kepala_sekolah': kepala_sekolah,
	}
	return render(request, 'Master_data/data_nilai_raport/detail.html',  context)

# cetak raport
def Laporan_raport_X(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X').values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
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
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='X', jurusan="Tata Boga")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)


	data_rap = Model_peringkat.objects.filter(kelas='X', jurusan="Tata Boga").aggregate(max=Max('nilai_raport'))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Tata Boga").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Tata Boga").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='X', nama_jurusan="Tata Boga").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
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
	# kriteria
	'kriteria': kriteria,
	'prestasi': prestasi,
	'ketidak_hadiran': ketidak_hadiran,
	'tanggal_sekarang': tanggal_sekarang,
	# kepala sekolah
	'kepala_sekolah': kepala_sekolah,
	}
	return render(request, 'Master_data/data_nilai_raport/raport_x.html',  context)


# raport kelas XI
@login_required(login_url=settings.LOGIN_URL)
def Data_raport_XI(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI').values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
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
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='A', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=None)


	# proses nilai raport cari kelompok B Wajib
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='B', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok C Peminatan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='C', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok Mulok
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='Mulok', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=None)

	# perbandingan nilai siswa-siswi
	
	# kelas X
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='XI', jurusan="Tata Boga")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)


	data_rap = Model_peringkat.objects.filter(kelas='XI', jurusan="Tata Boga").aggregate(max=Max('nilai_raport'))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI', nama_jurusan="Tata Boga").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI', nama_jurusan="Tata Boga").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI', nama_jurusan="Tata Boga").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
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
	return render(request, 'Master_data/data_nilai_raport/detail_xi.html',  context)

def Laporan_raport_2(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI').values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
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
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='A', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=None)


	# proses nilai raport cari kelompok B Wajib
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='B', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok C Peminatan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='C', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok Mulok
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='Mulok', nama_kelas='XI').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=None)

	# perbandingan nilai siswa-siswi
	
	# kelas X
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='XI', jurusan="Tata Boga")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)


	data_rap = Model_peringkat.objects.filter(kelas='XI', jurusan="Tata Boga").aggregate(max=Max('nilai_raport'))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI', nama_jurusan="Tata Boga").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI', nama_jurusan="Tata Boga").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XI', nama_jurusan="Tata Boga").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
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
	return render(request, 'Master_data/data_nilai_raport/raport_xi.html',  context)

# kelas XII
# raport kelas XI
@login_required(login_url=settings.LOGIN_URL)
def Data_raport_XII(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII').values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
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
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='A', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=None)


	# proses nilai raport cari kelompok B Wajib
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='B', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok C Peminatan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='C', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok Mulok
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='Mulok', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=None)

	# perbandingan nilai siswa-siswi
	
	# kelas X
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='XI', jurusan="Tata Boga")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)


	data_rap = Model_peringkat.objects.filter(kelas='XII', jurusan="Tata Boga").aggregate(max=Max('nilai_raport'))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII', nama_jurusan="Tata Boga").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII', nama_jurusan="Tata Boga").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII', nama_jurusan="Tata Boga").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
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
	return render(request, 'Master_data/data_nilai_raport/detail_xii.html',  context)

def Laporan_raport_3(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	kelompok_mapel = Model_nilairapot.objects.values('kelompok_mapel').distinct()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_raport = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII').values('nama_siswa','no_induk','nama_kelas','nama_jurusan').distinct()
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
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='A', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok = Model_nilairapot.objects.filter(no_induk=None)


	# proses nilai raport cari kelompok B Wajib
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='B', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_B = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok C Peminatan
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='C', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_C = Model_nilairapot.objects.filter(no_induk=None)

	# proses nilai raport cari kelompok Mulok
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=cari_data, kelompok_mapel='Mulok', nama_kelas='XII').values('nama_mapel','nilai_kkm','nilai_pengetahuan','nilai_keterampilan','deskripsi_pengetahuan','deskripsi_keterampilan').distinct()
	else:
		tampil_kelompok_mulok = Model_nilairapot.objects.filter(no_induk=None)

	# perbandingan nilai siswa-siswi
	
	# kelas X
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		chek_relasi = Model_peringkat.objects.filter(no_induk=cari_data, kelas='XI', jurusan="Tata Boga")
	else:
		chek_relasi = Model_peringkat.objects.filter(no_induk=None)


	data_rap = Model_peringkat.objects.filter(kelas='XII', jurusan="Tata Boga").aggregate(max=Max('nilai_raport'))

	# kriteria esktra
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		kriteria = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII', nama_jurusan="Tata Boga").values('no_induk','kegiatan_ekstra','keterangan_esktra').distinct().order_by('id')[:3]
	else:
		kriteria = Model_nilairapot.objects.filter(no_induk=None)

	# kriteria prestasi
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		prestasi = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII', nama_jurusan="Tata Boga").values('no_induk','prestasi','keterangan_prestasi').distinct().order_by('id')[:3]
	else:
		prestasi = Model_nilairapot.objects.filter(no_induk=None)	

	# ketidak hadiran
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		ketidak_hadiran = Model_nilairapot.objects.filter(no_induk=cari_data, nama_kelas='XII', nama_jurusan="Tata Boga").values('no_induk','jml_sakit','jml_izin','tanpa_keterangan','keterangan_raport').distinct().order_by('id')[:1]
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
	return render(request, 'Master_data/data_nilai_raport/raport_xii.html',  context)

# halaman menu laporan
@login_required(login_url=settings.LOGIN_URL)
def Menu_laporan_admin(request):
	data_kelas = Model_kelas.objects.all()
	data_tahun = Model_tahun_pelajaran.objects.all()
	select_jurusan = Model_jurusan.objects.all()	
	context = {	
	'select_jurusan': select_jurusan,
	'data_kelas': data_kelas,
	'data_tahun': data_tahun
	}
	return render(request, 'Master_data/laporan/menu.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_siswa(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'cari_jurusan' in request.GET:
		cari_jurusan=request.GET['cari_jurusan']
		cari_kelas=request.GET['cari_kelas']
		cari_tahun=request.GET['cari_tahun']
		lpsiswa = Model_siswa1.objects.filter(jurusan=cari_jurusan, kelas=cari_kelas, tahun_masuk=cari_tahun)
	else:
		lpsiswa = Model_siswa1.objects.filter(id=None)

	context = {		
	'lpsiswa': lpsiswa,
	'tanggal_sekarang': tanggal_sekarang
	}
	return render(request, 'Master_data/laporan/lp_siswa.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_guru(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'cari_jabatan' in request.GET:
		cari_jabatan=request.GET['cari_jabatan']
		lp_guru = Model_guru.objects.filter(jabatan=cari_jabatan)
	else:
		lp_guru = Model_guru.objects.filter(id=None)

	context = {		
	'lp_guru': lp_guru,
	'tanggal_sekarang': tanggal_sekarang
	}
	return render(request, 'Master_data/laporan/lp_guru.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_nilai(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'cari_jurusan' in request.GET:
		cari_jurusan=request.GET['cari_jurusan']
		cari_kelas=request.GET['cari_kelas']
		cari_noinduk=request.GET['cari_noinduk']
		lp_nilai = Model_nilairapot.objects.filter(nama_jurusan=cari_jurusan, nama_kelas=cari_kelas, no_induk=cari_noinduk)
	else:
		lp_nilai = Model_nilairapot.objects.filter(id=None)

	if 'cari_jurusan' in request.GET:
		cari_jurusan=request.GET['cari_jurusan']
		cari_kelas=request.GET['cari_kelas']
		cari_noinduk=request.GET['cari_noinduk']
		data = Model_nilairapot.objects.filter(nama_jurusan=cari_jurusan, nama_kelas=cari_kelas, no_induk=cari_noinduk).values('no_induk','nama_siswa','nama_jurusan','nama_kelas').distinct()
	else:
		data = Model_nilairapot.objects.filter(id=None)	

	context = {		
	'lp_nilai': lp_nilai,
	'tanggal_sekarang': tanggal_sekarang,
	'data': data,
	}
	return render(request, 'Master_data/laporan/lp_nilai.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_mapel(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	
	if 'cari_kelompok' in request.GET:
		cari_kelompok=request.GET['cari_kelompok']
		lp_mapel = Model_matapelajaran.objects.filter(kelompok_mapel=cari_kelompok)
	else:
		lp_mapel = Model_matapelajaran.objects.filter(id=None)

	# kelompok
	if 'cari_kelompok' in request.GET:
		cari_kelompok=request.GET['cari_kelompok']
		kl_mapel = Model_matapelajaran.objects.filter(kelompok_mapel=cari_kelompok).values('kelompok_mapel').distinct()
	else:
		kl_mapel = Model_matapelajaran.objects.filter(id=None)

	context = {		
	'lp_mapel': lp_mapel,
	'kl_mapel': kl_mapel,
	'tanggal_sekarang': tanggal_sekarang
	}
	return render(request, 'Master_data/laporan/lp_mapel.html',  context)

# ----------MASTER PEMBAYARAN----------
@login_required(login_url=settings.LOGIN_URL)
def Data_jenis_pembayaran(request):
	data_jenis = Model_jenis_pembayaran.objects.all()
	context = {	

	'data_jenis': data_jenis,
	}
	return render(request, 'Master_pembayaran/data_jenis/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_jenis_pembayaran(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if request.method == 'POST':
		Model_jenis_pembayaran.objects.create(
			jenis_pembayaran = request.POST['jenis_pembayaran'],
			nominal = request.POST['nominal'],
			keterangan = request.POST['keterangan'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Jenis/")	
	context = {	
	'tanggal_sekarang': tanggal_sekarang,
	}
	return render(request, 'Master_pembayaran/data_jenis/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_jenis_pembayaran(request, id_jenis):		
	edit_jenis = Model_jenis_pembayaran.objects.get(id=id_jenis)
	if request.method == 'POST':
			edit_jenis.jenis_pembayaran = request.POST.get('jenis_pembayaran')			
			edit_jenis.nominal = request.POST.get('nominal')
			edit_jenis.keterangan = request.POST.get('keterangan')
			edit_jenis.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Jenis')

	context = {'edit_jenis': edit_jenis}
	return render(request, 'Master_pembayaran/data_jenis/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_jenis_pembayaran(request, id_jenis):
	Model_jenis_pembayaran.objects.filter(id=id_jenis).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Jenis')
# pembayaran
@login_required(login_url=settings.LOGIN_URL)
def Data_pembayaran(request):
	data_pembayaran = Model_pembayaran_manajemen.objects.all()
	context = {	

	'data_pembayaran': data_pembayaran,
	}
	return render(request, 'Master_pembayaran/data_pembayaran/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_pembayaran(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	tahun_sekarang = strftime('%Y')
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_siswa = Model_siswa1.objects.filter(nis=cari_data)
	else:
		data_siswa = Model_siswa1.objects.filter(id=None)

	select_jenis = Model_jenis_pembayaran.objects.all()

	if request.method == 'POST':
		Model_pembayaran_manajemen.objects.create(
			nis = request.POST['nis'],
			nama_siswa = request.POST['nama_siswa'],
			kelas = request.POST['kelas'],
			jurusan = request.POST['jurusan'],
			jenis_pembayaran = request.POST['jenis_pembayaran'],
			total = request.POST['total'],
			nominal = request.POST['nominal'],
			jumlah_tanggungan = request.POST['jumlah_tanggungan'],
			semester = request.POST['semester'],
			tahun_akademik = request.POST['tahun_akademik'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Pembayaran/")	
	context = {	
	'tanggal_sekarang': tanggal_sekarang,
	'data_siswa': data_siswa,
	'select_jenis': select_jenis,
	'tahun_sekarang': tahun_sekarang
	}
	return render(request, 'Master_pembayaran/data_pembayaran/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_pembayaran(request, id_pembayaran):
	tanggal_sekarang = strftime('%d-%m-%Y')
	tahun_sekarang = strftime('%Y')
	select_jenis = Model_jenis_pembayaran.objects.all()

	edit_bayar = Model_pembayaran_manajemen.objects.get(id=id_pembayaran)
	if request.method == 'POST':
			edit_bayar.jenis_pembayaran = request.POST.get('jenis_pembayaran')
			edit_bayar.total = request.POST.get('total')
			edit_bayar.nominal = request.POST.get('nominal')
			edit_bayar.jumlah_tanggungan = request.POST.get('jumlah_tanggungan')
			edit_bayar.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Pembayaran')

	context = {
	'tanggal_sekarang': tanggal_sekarang,
	'edit_bayar': edit_bayar,
	'select_jenis': select_jenis,
	'tahun_sekarang': tahun_sekarang
	}
	return render(request, 'Master_pembayaran/data_pembayaran/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Cetak_pembayaran(request, id_pembayaran):
	tanggal_sekarang = strftime('%d-%m-%Y')
	tahun_sekarang = strftime('%Y')
	tampil = Model_pembayaran_manajemen.objects.get(id=id_pembayaran)

	context = {
	'tanggal_sekarang': tanggal_sekarang,
	'tampil': tampil,
	'tahun_sekarang': tahun_sekarang
	}
	return render(request, 'Master_pembayaran/data_pembayaran/nota.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_pembayaran(request, id_pembayaran):
	Model_pembayaran_manajemen.objects.filter(id=id_pembayaran).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Pembayaran')

# tanggungan
@login_required(login_url=settings.LOGIN_URL)
def Data_tanggungan(request):
	jenis = Model_jenis_pembayaran.objects.all()
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data_tanggungan = Model_pembayaran_manajemen.objects.filter(nis=cari_data)
	else:
		data_tanggungan = Model_pembayaran_manajemen.objects.filter(id=None)

	
	context = {	
	'jenis': jenis,
	'data_tanggungan': data_tanggungan,
	}
	return render(request, 'Master_pembayaran/data_tanggungan/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Menu_laporan_pembayaran(request):
	context = {	
	'menu': 'menu'
	}
	return render(request, 'Master_pembayaran/laporan/menu.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_pembayaran(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	data = Model_pembayaran_manajemen.objects.all()

	context = {	
	'menu': 'menu',
	'data': data,
	'tanggal_sekarang': tanggal_sekarang
	}
	return render(request, 'Master_pembayaran/laporan/lp_pembayaran.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_semester_akademik(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data = Model_pembayaran_manajemen.objects.filter(semester=cari_data)
	else:
		data = Model_pembayaran_manajemen.objects.filter(id=None)

	context = {	
	'menu': 'menu',
	'data': data,
	'tanggal_sekarang': tanggal_sekarang
	}
	return render(request, 'Master_pembayaran/laporan/lp_tahun.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Laporan_tanggungan(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'cari_data' in request.GET:
		cari_data=request.GET['cari_data']
		data = Model_pembayaran_manajemen.objects.filter(nis=cari_data)
	else:
		data = Model_pembayaran_manajemen.objects.filter(id=None)

	context = {	
	'menu': 'menu',
	'data': data,
	'tanggal_sekarang': tanggal_sekarang
	}
	return render(request, 'Master_pembayaran/laporan/lp_tanggungan.html',  context)


# -------------------------------------------------
# master pendaftaran PPDB USer
@login_required(login_url=settings.LOGIN_URL)
def Check_pendaftarab(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	data_register = Model_PPDB.objects.all()

	context = {		
	'tanggal_sekarang': tanggal_sekarang,
	'data_register': data_register
	}
	return render(request, 'Master_ppdb/data_register/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_pendaftaranpdb(request, id_daftar):		
	edit_pendaftaran = Model_PPDB.objects.get(id=id_daftar)
	if request.method == 'POST':		
			edit_pendaftaran.no_ktp = request.POST.get('no_ktp')
			edit_pendaftaran.nama_lengkap = request.POST.get('nama_lengkap')
			edit_pendaftaran.alamat = request.POST.get('alamat')
			edit_pendaftaran.jk = request.POST.get('jk')
			edit_pendaftaran.nohp = request.POST.get('nohp')
			edit_pendaftaran.username = request.POST.get('username')
			edit_pendaftaran.password = request.POST.get('password')
			edit_pendaftaran.save()		
			messages.info(request, 'Data Berhasil Di Edit..')
			return redirect('check_register')

	context = {'edit_pendaftaran': edit_pendaftaran}
	return render(request, 'Master_ppdb/data_register/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_pendaftaranpdb(request, id_daftar):
	Model_PPDB.objects.filter(id=id_daftar).delete()
	messages.info(request, 'Data Berhasil Di Hapus..')
	return redirect('check_register')

@login_required(login_url=settings.LOGIN_URL)
def Check_ppdb(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	check_siswa = Model_siswa1.objects.all()
	data_pendaftaran = Model_pendaftaran_pesertaPPDB.objects.all()

	context = {		
	'tanggal_sekarang': tanggal_sekarang,
	'data_pendaftaran': data_pendaftaran,
	'check_siswa': check_siswa,
	}
	return render(request, 'Master_ppdb/data_pendaftaran/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_penerimaanpdb(request, id_ppdb):		
	select_jurusan = Model_jurusan.objects.all()
	edit_pendaftaranppdb = Model_pendaftaran_pesertaPPDB.objects.get(id=id_ppdb)
	if request.method == 'POST':		
			edit_pendaftaranppdb.no_kk = request.POST.get('no_kk')
			edit_pendaftaranppdb.no_ktp = request.POST.get('no_ktp')
			edit_pendaftaranppdb.nama_lengkap = request.POST.get('nama_lengkap')
			edit_pendaftaranppdb.alamat = request.POST.get('alamat')
			edit_pendaftaranppdb.jk = request.POST.get('jk')
			edit_pendaftaranppdb.tempat_lahir = request.POST.get('tempat_lahir')
			edit_pendaftaranppdb.tanggal_lahir = request.POST.get('tanggal_lahir')
			edit_pendaftaranppdb.nohp = request.POST.get('nohp')
			edit_pendaftaranppdb.email = request.POST.get('email')
			edit_pendaftaranppdb.pendidikan_akhir = request.POST.get('pendidikan_akhir')
			edit_pendaftaranppdb.nama_ibu = request.POST.get('nama_ibu')
			edit_pendaftaranppdb.nama_ayah = request.POST.get('nama_ayah')
			edit_pendaftaranppdb.pekerjaan_ibu = request.POST.get('pekerjaan_ibu')
			edit_pendaftaranppdb.pekerjaan_ayah = request.POST.get('pekerjaan_ayah')
			edit_pendaftaranppdb.nama_jurusan = request.POST.get('nama_jurusan')
			edit_pendaftaranppdb.status_penerimaan = request.POST.get('status_penerimaan')
			edit_pendaftaranppdb.save()		
			messages.info(request, 'Data Berhasil Di Edit..')
			return redirect('check_ppdb')

	context = {
	'edit_pendaftaranppdb': edit_pendaftaranppdb,
	'select_jurusan': select_jurusan,
	}
	return render(request, 'Master_ppdb/data_pendaftaran/edit.html',  context)
@login_required(login_url=settings.LOGIN_URL)
def Edit_foto_penerimaanpdb(request, id_ppdb):	
	edit_pendaftaranppdb = Model_pendaftaran_pesertaPPDB.objects.get(id=id_ppdb)
	if request.method == 'POST':		
			edit_pendaftaranppdb.foto = request.FILES.get('foto')
			edit_pendaftaranppdb.save()		
			messages.info(request, 'Data Berhasil Di Edit..')
			return redirect('check_ppdb')

	context = {
	'edit_pendaftaranppdb': edit_pendaftaranppdb,
	}
	return render(request, 'Master_ppdb/data_pendaftaran/edit_foto.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Transfer_siswa(request, id_ppdb):	
	edit_pendaftaranppdb = Model_pendaftaran_pesertaPPDB.objects.get(id=id_ppdb)
	if request.method == 'POST':
		Model_siswa1.objects.create(
			nis = request.POST['nis'],
			nama_lengkap = request.POST['nama_lengkap'],
			jk = request.POST['jk'],			
			alamat = request.POST['alamat'],
			tempat_lahir = request.POST['tempat_lahir'],
			tanggal_lahir = request.POST['tanggal_lahir'],
			nohp = request.POST['nohp'],
			jurusan = request.POST['jurusan'],
			kelas = request.POST['kelas'],			
			foto = request.POST['foto'],			
			)
		Model_pendaftaran_pesertaPPDB.objects.filter(id=id_ppdb).delete()
		messages.info(request, 'Data Berhasil Di Transfer Ke Data Siswa..')
		return redirect('check_ppdb')

	context = {
	'edit_pendaftaranppdb': edit_pendaftaranppdb,
	}
	return render(request, 'Master_ppdb/data_pendaftaran/transfer_data.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_penerimaanpdb(request, id_ppdb):
	Model_pendaftaran_pesertaPPDB.objects.filter(id=id_ppdb).delete()
	messages.info(request, 'Data Berhasil Di Hapus..')
	return redirect('check_ppdb')

@login_required(login_url=settings.LOGIN_URL)
def Check_berkas(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	data_berkas = Model_BerkasPPDB.objects.all()

	context = {		
	'tanggal_sekarang': tanggal_sekarang,
	'data_berkas': data_berkas,
	}
	return render(request, 'Master_ppdb/data_berkas/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_berkas(request, id_berkas):
	Model_BerkasPPDB.objects.filter(id=id_berkas).delete()
	messages.info(request, 'Data Berhasil Di Hapus..')
	return redirect('check_berkas')

# soal
@login_required(login_url=settings.LOGIN_URL)
def Data_soal(request):
	data_soal = Model_tes_soalppdb.objects.all()
	context = {	

	'data_soal': data_soal,
	}
	return render(request, 'Master_ppdb/data_soal/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_soal(request):
	select_mapel = Model_matapelajaran.objects.all()
	if request.method == 'POST':
		Model_tes_soalppdb.objects.create(
			nama_mapel = request.POST['nama_mapel'],
			soal_mapel = request.POST['soal_mapel'],
			nilai_mapel = request.POST['nilai_mapel'],
			a = request.POST['a'],
			b = request.POST['b'],
			c = request.POST['c'],
			d = request.POST['d'],
			kunci_jawaban = request.POST['kunci_jawaban'],
			tanggal_tes = request.POST['tanggal_tes'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Soal_ppdb/")	
	context = {	
	'Tambah siswa': 'Tambah siswa',
	'select_mapel': select_mapel,
	}
	return render(request, 'Master_ppdb/data_soal/tambah.html', context)

@login_required(login_url=settings.LOGIN_URL)
def Edit_soal(request, id_soal):		
	select_mapel = Model_matapelajaran.objects.all()
	edit_soal = Model_tes_soalppdb.objects.get(id=id_soal)
	if request.method == 'POST':
			edit_soal.nama_mapel = request.POST.get('nama_mapel')			
			edit_soal.soal_mapel = request.POST.get('soal_mapel')
			edit_soal.nilai_mapel = request.POST.get('nilai_mapel')
			edit_soal.a = request.POST.get('a')
			edit_soal.b = request.POST.get('b')
			edit_soal.c = request.POST.get('c')
			edit_soal.d = request.POST.get('d')
			edit_soal.kunci_jawaban = request.POST.get('kunci_jawaban')
			edit_soal.tanggal_tes = request.POST.get('tanggal_tes')
			edit_soal.save()		
			messages.info(request, 'Data Berhasil Di Edit..?')
			return redirect('Soal_ppdb')

	context = {'edit_soal': edit_soal,'select_mapel': select_mapel}
	return render(request, 'Master_ppdb/data_soal/edit.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_soal(request, id_soal):
	Model_tes_soalppdb.objects.filter(id=id_soal).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Soal_ppdb')


# tes soal
@login_required(login_url=settings.LOGIN_URL)
def Data_tes_soal(request):
	data_tes = Model_tes_pesertadb1.objects.all()
	context = {	

	'data_tes': data_tes,
	}
	return render(request, 'Master_ppdb/data_tes/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Tambah_nilai_tes(request, id_nilai):			
	edit_nilai = Model_tes_pesertadb1.objects.get(id=id_nilai)
	if request.method == 'POST':
		Model_nilai_tes.objects.create(
			no_ktp = request.POST['no_ktp'],
			nama_lengkap = request.POST['nama_lengkap'],
			jumlah_nilai = request.POST['jumlah_nilai'],
			rata_nilai = request.POST['rata_nilai'],
			tanggal_tes = request.POST['tanggal_tes'],
			)
		messages.info(request, 'Data Berhasil Di Simpan..?')
		return HttpResponseRedirect("/Check_nilai/")

	context = {'edit_nilai': edit_nilai}
	return render(request, 'Master_ppdb/data_tes/tambah_nilai.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_tes_soal(request, id_tes):
	Model_tes_pesertadb1.objects.filter(id=id_tes).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Check_tes')

# nilai tes
@login_required(login_url=settings.LOGIN_URL)
def Nilai_tes_soal(request):
	data_nilai = Model_nilai_tes.objects.all()
	context = {	

	'data_nilai': data_nilai,
	}
	return render(request, 'Master_ppdb/data_nilai_tes/tabel.html',  context)

@login_required(login_url=settings.LOGIN_URL)
def Hapus_nilai_tes_soal(request, id_nilai):
	Model_nilai_tes.objects.filter(id=id_nilai).delete()
	messages.info(request, 'Data Berhasil Di Hapus..?')
	return redirect('Check_nilai')

@login_required(login_url=settings.LOGIN_URL)
def Menu_laporan_PPDB(request):
	data_kelas = Model_kelas.objects.all()
	select_jurusan = Model_jurusan.objects.all()	
	context = {	
	'select_jurusan': select_jurusan,
	'data_kelas': data_kelas,
	}
	return render(request, 'Master_ppdb/laporan/menu.html',  context)

def Laporan_ppdb(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	data_ppdb = Model_pendaftaran_pesertaPPDB.objects.all()
	context = {	
	'data_ppdb': data_ppdb,
	'tanggal_sekarang': tanggal_sekarang,
	}
	return render(request, 'Master_ppdb/laporan/lp_ppdb.html',  context)

def Laporan_nilai_ppdb(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	data_nilai = Model_nilai_tes.objects.all()
	context = {	
	'data_nilai': data_nilai,
	'tanggal_sekarang': tanggal_sekarang,
	}
	return render(request, 'Master_ppdb/laporan/lp_nilai.html',  context)


# -------------------------------------------------------------
# halaman pendaftaran PPDB
def Aplikasi_PPDB(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	}
	return render(request, 'Master_pendaftaran/index.html',  context)

def Pendftaran(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if request.method == 'POST':
		Model_PPDB.objects.create(
			no_ktp = request.POST['no_ktp'],
			nama_lengkap = request.POST['nama_lengkap'],
			alamat = request.POST['alamat'],
			jk = request.POST['jk'],
			nohp = request.POST['nohp'],
			username = request.POST['username'],
			password = request.POST['password'],
			)
		messages.info(request, 'Data Berhasil Terdaftar..?')
		return HttpResponseRedirect("/halaman_login/")

	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	}
	return render(request, 'Master_pendaftaran/daftar.html',  context)

def Halaman_login(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)
	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'login': login,
	
	}
	return render(request, 'Master_pendaftaran/login.html',  context)

def Login_ppdb(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)
	
	for berkas in login:
		no_ktp = berkas.no_ktp
	# check berkas
	check_data = Model_BerkasPPDB.objects.filter(no_ktp=no_ktp)

	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'login': login,
	'check_data': check_data
	}
	return render(request, 'Master_pendaftaran/Master_peserta/halaman.html',  context)

def Halaman_pendaftaran(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)

	# check data didik baru
	check_data = Model_pendaftaran_pesertaPPDB.objects.all()

	

	select_jurusan = Model_jurusan.objects.all()
	if request.method == 'POST':
		Model_pendaftaran_pesertaPPDB.objects.create(
			no_kk = request.POST['no_kk'],
			no_ktp = request.POST['no_ktp'],
			nama_lengkap = request.POST['nama_lengkap'],
			alamat = request.POST['alamat'],
			jk = request.POST['jk'],
			tempat_lahir = request.POST['tempat_lahir'],
			tanggal_lahir = request.POST['tanggal_lahir'],
			nohp = request.POST['nohp'],
			email = request.POST['email'],
			pendidikan_akhir = request.POST['pendidikan_akhir'],
			nama_ibu = request.POST['nama_ibu'],
			nama_ayah = request.POST['nama_ayah'],
			pekerjaan_ibu = request.POST['pekerjaan_ibu'],
			pekerjaan_ayah = request.POST['pekerjaan_ayah'],
			foto = request.FILES['foto'],
			nama_jurusan = request.POST['nama_jurusan'],
			)
		messages.info(request, 'Data Berhasil Terdaftar..?')
	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'select_jurusan': select_jurusan,
	'login': login,
	'check_data': check_data,
	}
	return render(request, 'Master_pendaftaran/Master_peserta/data/tambah_pendaftaran.html',  context)


def Halaman_berkas(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)

	if request.method == 'POST':
		Model_BerkasPPDB.objects.create(
			no_ktp = request.POST['no_ktp'],
			nama_lengkap = request.POST['nama_lengkap'],
			berkas_kk = request.FILES['berkas_kk'],
			berkas_ijazah = request.FILES['berkas_ijazah'],
			berkas_akte = request.FILES['berkas_akte'],
			)
		messages.info(request, 'Data Berhasil Tersimpan..?')
	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'login': login,
	}
	return render(request, 'Master_pendaftaran/Master_peserta/data/tambah_berkas.html',  context)


def Status_penerimaan(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)

	check_data = Model_pendaftaran_pesertaPPDB.objects.all()

	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'login': login,
	'check_data': check_data,
	}
	return render(request, 'Master_pendaftaran/Master_peserta/data/status_penerimaan.html',  context)

def Soal_tes(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)

	# soal
	soal = Model_tes_soalppdb.objects.all()

	if request.method == 'POST':
		for char in soal:
			Model_tes_pesertadb1.objects.create(
					no_ktp = request.POST['no_ktp'],
					nama_lengkap = request.POST['nama_lengkap'],
					nama_mapel = request.POST['nama_mapel'],
					soal_mapel = request.POST['soal_mapel'],
					jawaban = request.POST.getlist('jawaban'),
					tanggal_tes = request.POST['tanggal_tes']
					)			
			messages.info(request, 'Data Berhasil Tersimpan..?')

	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'login': login,
	'soal': soal,	
	}
	return render(request, 'Master_pendaftaran/Master_peserta/data/soal_tes.html',  context)

def Nilai_tes(request):
	tanggal_sekarang = strftime('%d-%m-%Y')
	if 'username' in request.GET:
		username=request.GET['username']
		password=request.GET['password']
		login = Model_PPDB.objects.filter(username=username, password=password)
	else:
		login = Model_PPDB.objects.filter(id=None)

	check_data = Model_nilai_tes.objects.all()

	context = {
	'Halaman': 'Aplikasi (PPDB)',
	'tanggal_sekarang': tanggal_sekarang,
	'login': login,
	'check_data': check_data,
	}
	return render(request, 'Master_pendaftaran/Master_peserta/data/nilai_tes.html',  context)