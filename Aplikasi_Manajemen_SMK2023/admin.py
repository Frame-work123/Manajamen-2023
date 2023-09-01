from django.contrib import admin

# Register your models here. daftar model yang telah kita buat
# from .models import Model_siswa, Model_kelas, Model_jurusan, Model_matapelajaran, Model_guru, Model_jadwall, Model_nilairapot, Model_peringkat, Model_PPDB, Model_pendaftaran_pesertaPPDB, Model_BerkasPPDB, Model_tes_pesertadb1, Model_tes_soalppdb, Model_nilai_tes, Model_jenis_pembayaran, Model_pembayaran_manajemen
from .models import *

admin.site.register(Model_siswa1)
admin.site.register(Model_kelas)
admin.site.register(Model_jurusan)
admin.site.register(Model_matapelajaran)
admin.site.register(Model_guru)
admin.site.register(Model_jadwall1)
admin.site.register(Model_nilairapot)
admin.site.register(Model_peringkat)
admin.site.register(Model_PPDB)
admin.site.register(Model_pendaftaran_pesertaPPDB)
admin.site.register(Model_BerkasPPDB)
admin.site.register(Model_tes_pesertadb1)
admin.site.register(Model_tes_soalppdb)
admin.site.register(Model_nilai_tes)
admin.site.register(Model_jenis_pembayaran)
admin.site.register(Model_pembayaran_manajemen)
admin.site.register(Model_tahun_pelajaran)