# from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from Aplikasi_Manajemen_SMK2023 import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
# from .views import index, HomeView, LogoutView, Data_kelas, Tambah_kelas, Edit_kelas, Hapus_kelas, Data_siswa, Tambah_siswa, Edit_siswa, Hapus_siswa, Edit_foto_siswa, Data_mapel, Tambah_mapel, Edit_mapel, Hapus_mapel, Data_guru, Tambah_guru, Edit_guru, Hapus_guru, Edit_foto_guru, Data_jurusan, Tambah_jurusan, Edit_jurusan, Hapus_jurusan, Data_jadwal, Tambah_jadwal, Edit_jadwal, Hapus_jadwal, View_jadwal, Laporan_jadwal, Data_nilai_raport, Tambah_nilai_raport, Edit_nilai_raport, Edit_keterangan_raport,Hapus_nilai_raport, Data_raport, Menu_laporan_admin, Laporan_siswa, Laporan_guru, Laporan_nilai, Laporan_mapel, Aplikasi_PPDB, Pendftaran, Login_ppdb, Halaman_login, Halaman_pendaftaran, Halaman_berkas, Status_penerimaan, Soal_tes
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('Home/', HomeView, name="Home"),
    path('logout/',LogoutView, name="logout"),
    # master data
    path('Kelas/',Data_kelas, name="Kelas"),
    path('Tambah_kelas/',Tambah_kelas, name="Tambah_kelas"),
    path('edit_kelas/<str:id_kls>',Edit_kelas, name="edit_kelas"),
    path('hapus_kelas/<str:id_kls>',Hapus_kelas, name="hapus_kelas"),
    # tahun ajaran
    path('Tahun/',Data_tahun, name="Tahun"),
    path('Tambah_tahun/',Tambah_tahun, name="Tambah_tahun"),
    path('edit_tahun/<str:id>',Edit_tahun, name="edit_tahun"),
    path('hapus_tahun/<str:id>',Hapus_tahun, name="hapus_tahun"),
    # data siswa
    path('Siswa/',Data_siswa, name="Siswa"),
    path('Tambah_siswa/',Tambah_siswa, name="Tambah_siswa"),
    path('edit_siswa/<str:id_siswa>',Edit_siswa, name="edit_siswa"),
    path('edit_foto_siswa/<str:id_siswa>',Edit_foto_siswa, name="edit_foto_siswa"),
    path('hapus_siswa/<str:id_siswa>',Hapus_siswa, name="hapus_siswa"),
    # data mata pelajaran
    path('Mapel/',Data_mapel, name="Mapel"),
    path('Tambah_mapel/',Tambah_mapel, name="Tambah_mapel"),
    path('edit_mapel/<str:id_mapel>',Edit_mapel, name="edit_mapel"),
    path('hapus_mapel/<str:id_mapel>',Hapus_mapel, name="hapus_mapel"),
    # data guru
    path('Guru/',Data_guru, name="Guru"),
    path('Tambah_guru/',Tambah_guru, name="Tambah_guru"),
    path('edit_guru/<str:id_guru>',Edit_guru, name="edit_guru"),
    path('edit_foto_guru/<str:id_guru>',Edit_foto_guru, name="edit_foto_guru"),
    path('hapus_guru/<str:id_guru>',Hapus_guru, name="hapus_guru"),
    # data jurusan
    path('Jurusan/',Data_jurusan, name="Jurusan"),
    path('Tambah_jurusan/',Tambah_jurusan, name="Tambah_jurusan"),
    path('edit_jurusan/<str:id_jurusan>',Edit_jurusan, name="edit_jurusan"),
    path('hapus_jurusan/<str:id_jurusan>',Hapus_jurusan, name="hapus_jurusan"),
    # data jadwal
    path('Jadwal/',Data_jadwal, name="Jadwal"),
    path('Tambah_jadwal/',Tambah_jadwal, name="Tambah_jadwal"),
    path('edit_jadwal/<str:id_jadwal>',Edit_jadwal, name="edit_jadwal"),
    path('hapus_jadwal/<str:id_jadwal>',Hapus_jadwal, name="hapus_jadwal"),
    path('view_jadwal/',View_jadwal, name="view_jadwal"),
    path('lp_jadwal/',Laporan_jadwal, name="lp_jadwal"),
    # data nilai raport
    path('Nilai/',Data_nilai_raport, name="Nilai"),
    path('Tambah_nilai/',Tambah_nilai_raport, name="Tambah_nilai"),
    path('edit_nilai/<str:id_nilai>',Edit_nilai_raport, name="edit_nilai"),
    path('edit_keterangan/<str:id_nilai>',Edit_keterangan_raport, name="edit_keterangan"),
    path('hapus_nilai/<str:id_nilai>',Hapus_nilai_raport, name="hapus_nilai"),
    # detail nilai
    path('Detail/',Data_raport, name="Detail"),
    path('laporan_X/',Laporan_raport_X, name="laporan_X"),    

    path('Raport_XI/',Data_raport_XI, name="Raport_XI"),
    path('claporan_XI/',Laporan_raport_2, name="claporan_XI"),

    path('Raport_XII/',Data_raport_XII, name="Raport_XII"),
    path('cetak_Raport_XII/',Laporan_raport_3, name="cetak_Raport_XII"),

    # menu laporan admin
    path('Menu/',Menu_laporan_admin, name="Menu"),
    path('Lp_siswa/',Laporan_siswa, name="Lp_siswa"),
    path('Lp_guru/',Laporan_guru, name="Lp_guru"),
    path('Lp_nilai/',Laporan_nilai, name="Lp_nilai"),
    path('Lp_mapel/',Laporan_mapel, name="Lp_mapel"),

    # master PPDB
    path('check_register/',Check_pendaftarab, name="check_register"),
    path('edit_check_daftar/<str:id_daftar>',Edit_pendaftaranpdb, name="edit_check_daftar"),
    path('hapus_check_daftar/<str:id_daftar>',Hapus_pendaftaranpdb, name="hapus_check_daftar"),
    # data ppdb
    path('check_ppdb/',Check_ppdb, name="check_ppdb"),
    path('edit_ppdb/<str:id_ppdb>',Edit_penerimaanpdb, name="edit_ppdb"),
    path('edit_foto_ppdb/<str:id_ppdb>',Edit_foto_penerimaanpdb, name="edit_foto_ppdb"),
    path('transfer_data/<str:id_ppdb>',Transfer_siswa, name="transfer_data"),
    path('hapus_ppdb/<str:id_ppdb>',Hapus_penerimaanpdb, name="hapus_ppdb"),
    # berkas data
    path('check_berkas/',Check_berkas, name="check_berkas"),
    path('hapus_berkas/<str:id_berkas>',Hapus_berkas, name="hapus_berkas"),
    # data soal
    path('Soal_ppdb/',Data_soal, name="Soal_ppdb"),
    path('Tambah_soal/',Tambah_soal, name="Tambah_soal"),
    path('edit_soal/<str:id_soal>',Edit_soal, name="edit_soal"),
    path('hapus_soal/<str:id_soal>',Hapus_soal, name="hapus_soal"),
    # tes soal
    path('Check_tes/',Data_tes_soal, name="Check_tes"),
    path('hapus_tes_soal/<str:id_tes>',Hapus_tes_soal, name="hapus_tes_soal"),
    path('tambah_nilai/<str:id_nilai>',Tambah_nilai_tes, name="tambah_nilai"),
    # nilai tes
    path('Check_nilai/',Nilai_tes_soal, name="Check_nilai"),
    path('hapus_nilai_tes_soal/<str:id_nilai>',Hapus_nilai_tes_soal, name="hapus_nilai_tes_soal"),
    # menu laporan ppdb
    path('menu_laporan/',Menu_laporan_PPDB, name="menu_laporan"),
    path('laporan_ppdb/',Laporan_ppdb, name="laporan_ppdb"),
    path('laporan_nilai_ppdb/',Laporan_nilai_ppdb, name="laporan_nilai_ppdb"),


    # MASTER PEMBAYARAN
    path('Jenis/',Data_jenis_pembayaran, name="Jenis"),
    path('Tambah_jenis/',Tambah_jenis_pembayaran, name="Tambah_jenis"),
    path('edit_jenis/<str:id_jenis>',Edit_jenis_pembayaran, name="edit_jenis"),
    path('hapus_jenis/<str:id_jenis>',Hapus_jenis_pembayaran, name="hapus_jenis"),
    # pembayaran
    path('Pembayaran/',Data_pembayaran, name="Pembayaran"),
    path('Tambah_pembayaran/',Tambah_pembayaran, name="Tambah_pembayaran"),
    path('edit_pembayaran/<str:id_pembayaran>',Edit_pembayaran, name="edit_pembayaran"),
    path('cetak_pembayaran/<str:id_pembayaran>',Cetak_pembayaran, name="cetak_pembayaran"),
    path('hapus_pembayaran/<str:id_pembayaran>',Hapus_pembayaran, name="hapus_pembayaran"),
    # tanggungan
    path('tanggungan/',Data_tanggungan, name="tanggungan"),
    # laporang
    path('Menu_lp_pembayaran/',Menu_laporan_pembayaran, name="Menu_lp_pembayaran"),
    path('lp_pembayaran/',Laporan_pembayaran, name="lp_pembayaran"),
    path('lp_semester/',Laporan_semester_akademik, name="lp_semester"),
    path('lp_tanggungan/',Laporan_tanggungan, name="lp_tanggungan"),



    # ----------------------------------------------------
    # halaman (PPDB)
    path('Website/',Aplikasi_PPDB, name="Website"),
    path('Daftar/',Pendftaran, name="Daftar"),
    path('halaman_login/',Halaman_login, name="halaman_login"),
    path('Login_daftar/',Login_ppdb, name="Login_daftar"),
    path('pendaftaran_baru/',Halaman_pendaftaran, name="pendaftaran_baru"),
    path('Berkas_daftar/',Halaman_berkas, name="Berkas_daftar"),
    path('status_penerimaan/',Status_penerimaan, name="status_penerimaan"),
    path('soal_ujian/',Soal_tes, name="soal_ujian"),
    path('nilai_ujian/',Nilai_tes, name="nilai_ujian"),
    # message

    path('admin/', admin.site.urls),
]

if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)