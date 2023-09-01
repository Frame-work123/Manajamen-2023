from django.http import HttpResponse
from django.shortcuts import redirect

#@tolakhalaman_ini
def tolakhalaman_ini(fungsi_awal):
	def perubahan_halaman(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('Home')
		else:
			return fungsi_awal(request, *args, **kwargs)
	return perubahan_halaman

def ijinkan_pengguna(yang_diizinkan=[]):
	def aturan(fungsi_awal):
		def perubahan_halaman(request, *args, **kwargs):
			# print('Nama User', yang_diizinkan )
			 group = None
			 if request.user.groups.exists():
			 	group = request.user.groups.all()[0].name
			 if group in yang_diizinkan :
			 	return fungsi_awal(request, *args, **kwargs)
			 else:
			 	return HttpResponse('<h2><center>Anda Tidak Memiliki Hak Akses Pada Halaman ini</center></h2>')
			 	# return redirect('info_pesan')

		return perubahan_halaman
	return aturan	

def pilihan_login(fungsi_awal):
	def perubahan_halaman(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		if group == 'Admin':
			return redirect('Home')
		if group == 'Admin':
			return fungsi_awal(request, *args, **kwargs)
	return perubahan_halaman