from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Model_kelas(models.Model):
	nama_kelas	= models.CharField(max_length = 1200)
	kapasitas	=models.CharField(max_length = 20)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nis)
	class Meta:
		db_table = "Model_kelas"	
  
class Model_tahun_pelajaran(models.Model):
	tahun	= models.CharField(max_length = 1200)
	semester	=models.CharField(max_length = 20)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nis)
	class Meta:
		db_table = "Model_tahun_pelajaran"	

class Model_jurusan(models.Model):
	nama_jurusan	= models.CharField(max_length = 1200)
	keterangan	=models.CharField(max_length = 2000)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nama_jurusan)
	class Meta:
		db_table = "Model_jurusan"

class Model_siswa1(models.Model):
	nis	= models.CharField(max_length = 1200)
	nama_lengkap	=models.CharField(max_length = 1200)
	jk	=models.CharField(max_length = 25)
	alamat	=models.CharField(max_length = 1250)
	tempat_lahir	=models.CharField(max_length = 12000)	
	tanggal_lahir	=models.CharField(max_length = 25)	
	nohp	=models.CharField(max_length = 25)	
	jurusan	=models.CharField(max_length = 250)	
	kelas	=models.CharField(max_length = 50)	
	foto	=models.ImageField(upload_to ='Berkas/', null=True)	
	tahun_masuk	=models.CharField(max_length = 50)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nis)
	class Meta:
		db_table = "Model_siswa1"

class Model_matapelajaran(models.Model):
	kode_mapel	= models.CharField(max_length = 25)
	nama_mapel	=models.CharField(max_length = 2000)
	keterangan	=models.CharField(max_length = 2000)
	kelompok_mapel	=models.CharField(max_length = 50)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.kode_mapel)
	class Meta:
		db_table = "Model_matapelajaran"

class Model_guru(models.Model):
	nidn	= models.CharField(max_length = 25)
	nama	=models.CharField(max_length = 2000)
	alamat	=models.CharField(max_length = 2000)
	tempat_lahir	=models.CharField(max_length = 2000)
	jk	=models.CharField(max_length = 25)
	nohp	=models.CharField(max_length = 15)
	jabatan	=models.CharField(max_length = 250)
	foto	=models.ImageField(upload_to ='Berkas/', null=True)	

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nidn)
	class Meta:
		db_table = "Model_guru"

class Model_jadwall1(models.Model):
	nama_jadwal	= models.CharField(max_length = 1200)
	tanggal_jadwal	=models.CharField(max_length = 15)
	hari	=models.CharField(max_length = 25)
	nama_mapel	=models.CharField(max_length = 2000)
	kode_guru	=models.CharField(max_length = 1)
	nama_guru	=models.CharField(max_length = 2000)
	jurusan	=models.CharField(max_length = 2000)
	kelas	=models.CharField(max_length = 6)
	jam_mapel	=models.CharField(max_length = 12)
	jam_masuk	=models.CharField(max_length = 12)
	jam_istirahat	=models.CharField(max_length = 12)
	keterangan	=models.CharField(max_length = 2000)
	#  
	keterangan_jadwal =models.CharField(max_length = 2000)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nama_jadwal)
	class Meta:
		db_table = "Model_jadwall1"

class Model_nilairapot(models.Model):
	nama_siswa	= models.CharField(max_length = 1200)
	no_induk	=models.CharField(max_length = 11)
	nama_kelas	= models.CharField(max_length = 12)
	nama_jurusan	= models.CharField(max_length = 1200)
	nama_mapel	= models.CharField(max_length = 1200)
	kelompok_mapel	= models.CharField(max_length = 1200)
	nilai_pengetahuan	= models.CharField(max_length = 12)
	deskripsi_pengetahuan	= models.CharField(max_length = 1200)
	nilai_keterampilan	= models.CharField(max_length = 12)
	deskripsi_keterampilan	= models.CharField(max_length = 1200)
	nilai_kkm	= models.CharField(max_length = 12)
	jumlah_nilai	= models.CharField(max_length = 12)
	rata_rata	= models.CharField(max_length = 12)
	# tambah ekstra kurikuler
	kegiatan_ekstra	= models.CharField(max_length = 1200)
	keterangan_esktra	= models.CharField(max_length = 1200)
	# prestasi
	prestasi	= models.CharField(max_length = 1200)
	keterangan_prestasi	= models.CharField(max_length = 1200)
	# ketidak hadiran
	jml_sakit	= models.CharField(max_length = 12)
	jml_izin	= models.CharField(max_length = 12)
	tanpa_keterangan	= models.CharField(max_length = 12)
	# keputusan
	keterangan_raport	= models.CharField(max_length = 1200)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_induk)
	class Meta:
		db_table = "Model_nilairapot"

class Model_peringkat(models.Model):
	no_induk	= models.CharField(max_length = 1200)
	nama_siswa	=models.CharField(max_length = 2000)
	kelas	=models.CharField(max_length = 2000)
	jurusan	=models.CharField(max_length = 2000)
	nilai_raport	=models.CharField(max_length = 2000)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_induk)
	class Meta:
		db_table = "Model_peringkat"

class Model_PPDB(models.Model):
	no_ktp	= models.CharField(max_length = 16)
	nama_lengkap	= models.CharField(max_length = 1200)
	alamat	= models.CharField(max_length = 1200)
	jk	= models.CharField(max_length = 25)
	nohp	= models.CharField(max_length = 25)
	username	= models.CharField(max_length = 250)
	password	= models.CharField(max_length = 250)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_ktp)
	class Meta:
		db_table = "Model_PPDB"

class Model_pendaftaran_pesertaPPDB(models.Model):
	no_kk	= models.CharField(max_length = 16)
	no_ktp	= models.CharField(max_length = 16)
	nama_lengkap	= models.CharField(max_length = 1200)
	alamat	= models.CharField(max_length = 1200)
	jk	= models.CharField(max_length = 25)
	tempat_lahir	= models.CharField(max_length = 1200)
	tanggal_lahir	= models.CharField(max_length = 25)
	nohp	= models.CharField(max_length = 13)
	email	= models.CharField(max_length = 1200)
	pendidikan_akhir	= models.CharField(max_length = 1200)
	nama_ibu	= models.CharField(max_length = 1200)
	nama_ayah	= models.CharField(max_length = 1200)
	pekerjaan_ibu	= models.CharField(max_length = 1200)
	pekerjaan_ayah	= models.CharField(max_length = 1200)
	foto	=models.ImageField(upload_to ='Berkas/', null=True)	
	nama_jurusan	= models.CharField(max_length = 1200)
	status_penerimaan	= models.CharField(max_length = 1200)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_kk)
	class Meta:
		db_table = "Model_pendaftaran_pesertaPPDB"	

class Model_BerkasPPDB(models.Model):
	no_ktp	= models.CharField(max_length = 1200)
	nama_lengkap	= models.CharField(max_length = 1200)
	berkas_kk	=models.ImageField(upload_to ='Berkas/', null=True)
	berkas_ijazah	=models.ImageField(upload_to ='Berkas/', null=True)
	berkas_akte	=models.ImageField(upload_to ='Berkas/', null=True)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_ktp)	
	class Meta:
		db_table = "Model_BerkasPPDB"

class Model_tes_pesertadb1(models.Model):
	no_ktp	= models.CharField(max_length = 1200)
	nama_lengkap	= models.CharField(max_length = 1200)
	nama_mapel	= models.CharField(max_length = 1200)
	soal_mapel	= models.CharField(max_length = 1200)
	jawaban	= models.CharField(max_length = 1200)
	tanggal_tes	= models.CharField(max_length = 1200)

	

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_ktp)	
	class Meta:
		db_table = "Model_tes_pesertadb1"

class Model_tes_soalppdb(models.Model):	
	nama_mapel	= models.CharField(max_length = 1200)
	soal_mapel	= models.CharField(max_length = 1200)
	nilai_mapel	= models.CharField(max_length = 1200)
	a	= models.CharField(max_length = 1200)
	b	= models.CharField(max_length = 1200)
	c	= models.CharField(max_length = 1200)
	d	= models.CharField(max_length = 1200)
	kunci_jawaban	= models.CharField(max_length = 1200)
	tanggal_tes	= models.CharField(max_length = 1200)
	

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nama_mapel)	
	class Meta:
		db_table = "Model_tes_soalppdb"

class Model_nilai_tes(models.Model):
	no_ktp	= models.CharField(max_length = 1200)
	nama_lengkap	= models.CharField(max_length = 1200)	
	jumlah_nilai	= models.CharField(max_length = 1200)
	rata_nilai	= models.CharField(max_length = 1200)
	tanggal_tes	= models.CharField(max_length = 1200)

	

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.no_ktp)	
	class Meta:
		db_table = "Model_nilai_tes"

class Model_jenis_pembayaran(models.Model):
	jenis_pembayaran	= models.CharField(max_length = 1200)
	nominal	=models.CharField(max_length = 20)
	keterangan	= models.CharField(max_length = 1200)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nis)
	class Meta:
		db_table = "Model_jenis_pembayaran"
# khusus peringkat raport
# pendagftaran peserta didik baru
class Model_pembayaran_manajemen(models.Model):
	nis	=models.CharField(max_length = 20)
	nama_siswa	=models.CharField(max_length = 20)
	kelas	=models.CharField(max_length = 20)
	jurusan	=models.CharField(max_length = 20)
	jenis_pembayaran	= models.CharField(max_length = 1200)
	total	=models.CharField(max_length = 120)
	nominal	=models.CharField(max_length = 20)
	jumlah_tanggungan	=models.CharField(max_length = 20)
	semester	=models.CharField(max_length = 20)
	tahun_akademik	=models.CharField(max_length = 20)

	published = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
			
	def __str__(self):
		return "{}.{}".format(self.id, self.nis)
	class Meta:
		db_table = "Model_pembayaran_manajemen"

