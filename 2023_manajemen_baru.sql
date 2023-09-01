-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 19 Agu 2023 pada 07.53
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `2023_manajemen_baru`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(3, 'Pembayaran'),
(2, 'User');

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add model_kelas', 1, 'add_model_kelas'),
(2, 'Can change model_kelas', 1, 'change_model_kelas'),
(3, 'Can delete model_kelas', 1, 'delete_model_kelas'),
(4, 'Can view model_kelas', 1, 'view_model_kelas'),
(5, 'Can add model_tahun_pelajaran', 2, 'add_model_tahun_pelajaran'),
(6, 'Can change model_tahun_pelajaran', 2, 'change_model_tahun_pelajaran'),
(7, 'Can delete model_tahun_pelajaran', 2, 'delete_model_tahun_pelajaran'),
(8, 'Can view model_tahun_pelajaran', 2, 'view_model_tahun_pelajaran'),
(9, 'Can add model_jurusan', 3, 'add_model_jurusan'),
(10, 'Can change model_jurusan', 3, 'change_model_jurusan'),
(11, 'Can delete model_jurusan', 3, 'delete_model_jurusan'),
(12, 'Can view model_jurusan', 3, 'view_model_jurusan'),
(13, 'Can add model_siswa1', 4, 'add_model_siswa1'),
(14, 'Can change model_siswa1', 4, 'change_model_siswa1'),
(15, 'Can delete model_siswa1', 4, 'delete_model_siswa1'),
(16, 'Can view model_siswa1', 4, 'view_model_siswa1'),
(17, 'Can add model_matapelajaran', 5, 'add_model_matapelajaran'),
(18, 'Can change model_matapelajaran', 5, 'change_model_matapelajaran'),
(19, 'Can delete model_matapelajaran', 5, 'delete_model_matapelajaran'),
(20, 'Can view model_matapelajaran', 5, 'view_model_matapelajaran'),
(21, 'Can add model_guru', 6, 'add_model_guru'),
(22, 'Can change model_guru', 6, 'change_model_guru'),
(23, 'Can delete model_guru', 6, 'delete_model_guru'),
(24, 'Can view model_guru', 6, 'view_model_guru'),
(25, 'Can add model_jadwall1', 7, 'add_model_jadwall1'),
(26, 'Can change model_jadwall1', 7, 'change_model_jadwall1'),
(27, 'Can delete model_jadwall1', 7, 'delete_model_jadwall1'),
(28, 'Can view model_jadwall1', 7, 'view_model_jadwall1'),
(29, 'Can add model_nilairapot', 8, 'add_model_nilairapot'),
(30, 'Can change model_nilairapot', 8, 'change_model_nilairapot'),
(31, 'Can delete model_nilairapot', 8, 'delete_model_nilairapot'),
(32, 'Can view model_nilairapot', 8, 'view_model_nilairapot'),
(33, 'Can add model_peringkat', 9, 'add_model_peringkat'),
(34, 'Can change model_peringkat', 9, 'change_model_peringkat'),
(35, 'Can delete model_peringkat', 9, 'delete_model_peringkat'),
(36, 'Can view model_peringkat', 9, 'view_model_peringkat'),
(37, 'Can add model_ppdb', 10, 'add_model_ppdb'),
(38, 'Can change model_ppdb', 10, 'change_model_ppdb'),
(39, 'Can delete model_ppdb', 10, 'delete_model_ppdb'),
(40, 'Can view model_ppdb', 10, 'view_model_ppdb'),
(41, 'Can add model_pendaftaran_peserta ppdb', 11, 'add_model_pendaftaran_pesertappdb'),
(42, 'Can change model_pendaftaran_peserta ppdb', 11, 'change_model_pendaftaran_pesertappdb'),
(43, 'Can delete model_pendaftaran_peserta ppdb', 11, 'delete_model_pendaftaran_pesertappdb'),
(44, 'Can view model_pendaftaran_peserta ppdb', 11, 'view_model_pendaftaran_pesertappdb'),
(45, 'Can add model_ berkas ppdb', 12, 'add_model_berkasppdb'),
(46, 'Can change model_ berkas ppdb', 12, 'change_model_berkasppdb'),
(47, 'Can delete model_ berkas ppdb', 12, 'delete_model_berkasppdb'),
(48, 'Can view model_ berkas ppdb', 12, 'view_model_berkasppdb'),
(49, 'Can add model_tes_pesertadb1', 13, 'add_model_tes_pesertadb1'),
(50, 'Can change model_tes_pesertadb1', 13, 'change_model_tes_pesertadb1'),
(51, 'Can delete model_tes_pesertadb1', 13, 'delete_model_tes_pesertadb1'),
(52, 'Can view model_tes_pesertadb1', 13, 'view_model_tes_pesertadb1'),
(53, 'Can add model_tes_soalppdb', 14, 'add_model_tes_soalppdb'),
(54, 'Can change model_tes_soalppdb', 14, 'change_model_tes_soalppdb'),
(55, 'Can delete model_tes_soalppdb', 14, 'delete_model_tes_soalppdb'),
(56, 'Can view model_tes_soalppdb', 14, 'view_model_tes_soalppdb'),
(57, 'Can add model_nilai_tes', 15, 'add_model_nilai_tes'),
(58, 'Can change model_nilai_tes', 15, 'change_model_nilai_tes'),
(59, 'Can delete model_nilai_tes', 15, 'delete_model_nilai_tes'),
(60, 'Can view model_nilai_tes', 15, 'view_model_nilai_tes'),
(61, 'Can add model_jenis_pembayaran', 16, 'add_model_jenis_pembayaran'),
(62, 'Can change model_jenis_pembayaran', 16, 'change_model_jenis_pembayaran'),
(63, 'Can delete model_jenis_pembayaran', 16, 'delete_model_jenis_pembayaran'),
(64, 'Can view model_jenis_pembayaran', 16, 'view_model_jenis_pembayaran'),
(65, 'Can add model_pembayaran_manajemen', 17, 'add_model_pembayaran_manajemen'),
(66, 'Can change model_pembayaran_manajemen', 17, 'change_model_pembayaran_manajemen'),
(67, 'Can delete model_pembayaran_manajemen', 17, 'delete_model_pembayaran_manajemen'),
(68, 'Can view model_pembayaran_manajemen', 17, 'view_model_pembayaran_manajemen'),
(69, 'Can add log entry', 18, 'add_logentry'),
(70, 'Can change log entry', 18, 'change_logentry'),
(71, 'Can delete log entry', 18, 'delete_logentry'),
(72, 'Can view log entry', 18, 'view_logentry'),
(73, 'Can add permission', 19, 'add_permission'),
(74, 'Can change permission', 19, 'change_permission'),
(75, 'Can delete permission', 19, 'delete_permission'),
(76, 'Can view permission', 19, 'view_permission'),
(77, 'Can add group', 20, 'add_group'),
(78, 'Can change group', 20, 'change_group'),
(79, 'Can delete group', 20, 'delete_group'),
(80, 'Can view group', 20, 'view_group'),
(81, 'Can add user', 21, 'add_user'),
(82, 'Can change user', 21, 'change_user'),
(83, 'Can delete user', 21, 'delete_user'),
(84, 'Can view user', 21, 'view_user'),
(85, 'Can add content type', 22, 'add_contenttype'),
(86, 'Can change content type', 22, 'change_contenttype'),
(87, 'Can delete content type', 22, 'delete_contenttype'),
(88, 'Can view content type', 22, 'view_contenttype'),
(89, 'Can add session', 23, 'add_session'),
(90, 'Can change session', 23, 'change_session'),
(91, 'Can delete session', 23, 'delete_session'),
(92, 'Can view session', 23, 'view_session');

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$390000$3qxbrxBXFI1PuqMP5fplzC$Z+j1he2NERIVPmvCH7//oasbXvTuj0j0a57wj5FgKOg=', '2023-08-19 05:50:49.366447', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2023-08-06 10:58:43.000000'),
(2, 'pbkdf2_sha256$390000$6gwlgdwJLpAltlu7Tk4U3c$k55v3nZy54vzUhWWJxw2TJWKTy4vGI0NILSDuNQKTmM=', '2023-08-18 16:56:26.693963', 0, 'bayar@gmail.com', '', '', '', 0, 1, '2023-08-18 06:26:50.000000'),
(3, 'pbkdf2_sha256$390000$FqF8JfbUWKUURhAExhSVoe$MJUci8hbC44gYNQdFJi03mT7xBQvy4iX4aaT7jT0v28=', '2023-08-18 17:24:05.114311', 0, 'ppdb@gmail.com', '', '', '', 0, 1, '2023-08-18 06:30:20.000000');

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 3),
(3, 3, 2);

-- --------------------------------------------------------

--
-- Struktur dari tabel `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-08-06 10:59:34.357120', '1', 'Admin', 1, '[{\"added\": {}}]', 20, 1),
(2, '2023-08-06 10:59:42.048210', '2', 'User', 1, '[{\"added\": {}}]', 20, 1),
(3, '2023-08-06 10:59:49.052353', '3', 'Pembayaran', 1, '[{\"added\": {}}]', 20, 1),
(4, '2023-08-06 11:00:12.824891', '1', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 21, 1),
(5, '2023-08-18 06:26:50.544268', '2', 'bayar@gmail.com', 1, '[{\"added\": {}}]', 21, 1),
(6, '2023-08-18 06:27:04.048439', '2', 'bayar@gmail.com', 2, '[]', 21, 1),
(7, '2023-08-18 06:27:59.967420', '2', 'bayar@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 21, 1),
(8, '2023-08-18 06:30:21.169897', '3', 'ppdb@gmail.com', 1, '[{\"added\": {}}]', 21, 1),
(9, '2023-08-18 06:30:53.933373', '3', 'ppdb@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 21, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(18, 'admin', 'logentry'),
(12, 'Aplikasi_Manajemen_SMK2023', 'model_berkasppdb'),
(6, 'Aplikasi_Manajemen_SMK2023', 'model_guru'),
(7, 'Aplikasi_Manajemen_SMK2023', 'model_jadwall1'),
(16, 'Aplikasi_Manajemen_SMK2023', 'model_jenis_pembayaran'),
(3, 'Aplikasi_Manajemen_SMK2023', 'model_jurusan'),
(1, 'Aplikasi_Manajemen_SMK2023', 'model_kelas'),
(5, 'Aplikasi_Manajemen_SMK2023', 'model_matapelajaran'),
(8, 'Aplikasi_Manajemen_SMK2023', 'model_nilairapot'),
(15, 'Aplikasi_Manajemen_SMK2023', 'model_nilai_tes'),
(17, 'Aplikasi_Manajemen_SMK2023', 'model_pembayaran_manajemen'),
(11, 'Aplikasi_Manajemen_SMK2023', 'model_pendaftaran_pesertappdb'),
(9, 'Aplikasi_Manajemen_SMK2023', 'model_peringkat'),
(10, 'Aplikasi_Manajemen_SMK2023', 'model_ppdb'),
(4, 'Aplikasi_Manajemen_SMK2023', 'model_siswa1'),
(2, 'Aplikasi_Manajemen_SMK2023', 'model_tahun_pelajaran'),
(13, 'Aplikasi_Manajemen_SMK2023', 'model_tes_pesertadb1'),
(14, 'Aplikasi_Manajemen_SMK2023', 'model_tes_soalppdb'),
(20, 'auth', 'group'),
(19, 'auth', 'permission'),
(21, 'auth', 'user'),
(22, 'contenttypes', 'contenttype'),
(23, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-08-06 10:56:56.879561'),
(2, 'auth', '0001_initial', '2023-08-06 10:57:02.398834'),
(3, 'admin', '0001_initial', '2023-08-06 10:57:03.789554'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-08-06 10:57:03.852065'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-08-06 10:57:03.898980'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-08-06 10:57:04.914964'),
(7, 'auth', '0002_alter_permission_name_max_length', '2023-08-06 10:57:05.586629'),
(8, 'auth', '0003_alter_user_email_max_length', '2023-08-06 10:57:05.711919'),
(9, 'auth', '0004_alter_user_username_opts', '2023-08-06 10:57:05.758567'),
(10, 'auth', '0005_alter_user_last_login_null', '2023-08-06 10:57:06.086677'),
(11, 'auth', '0006_require_contenttypes_0002', '2023-08-06 10:57:06.102585'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2023-08-06 10:57:06.164817'),
(13, 'auth', '0008_alter_user_username_max_length', '2023-08-06 10:57:06.243236'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2023-08-06 10:57:06.336742'),
(15, 'auth', '0010_alter_group_name_max_length', '2023-08-06 10:57:06.414881'),
(16, 'auth', '0011_update_proxy_permissions', '2023-08-06 10:57:06.602422'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2023-08-06 10:57:06.665080'),
(18, 'sessions', '0001_initial', '2023-08-06 10:57:06.930526');

-- --------------------------------------------------------

--
-- Struktur dari tabel `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('33y2rhpiihq7crkansoz81ctj4gqlj68', '.eJxVjEEOwiAQRe_C2pAy0AIu3XsGMgyMVA0kpV0Z765NutDtf-_9lwi4rSVsPS9hTuIslDj9bhHpkesO0h3rrUlqdV3mKHdFHrTLa0v5eTncv4OCvXxrq_Sk06ANJ2OAfRyzc0jAygKDRqaYvCeO2lmalFGkDAwWRmsyOrLi_QHbezel:1qXErJ:lBoVq4Z55zx7YGEIlkP9LMrp_-nYhho_dWQGfz-CtyM', '2023-09-02 05:50:49.454457');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_berkasppdb`
--

CREATE TABLE `model_berkasppdb` (
  `id` bigint(20) NOT NULL,
  `no_ktp` varchar(1200) NOT NULL,
  `nama_lengkap` varchar(1200) NOT NULL,
  `berkas_kk` varchar(100) DEFAULT NULL,
  `berkas_ijazah` varchar(100) DEFAULT NULL,
  `berkas_akte` varchar(100) DEFAULT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_berkasppdb`
--

INSERT INTO `model_berkasppdb` (`id`, `no_ktp`, `nama_lengkap`, `berkas_kk`, `berkas_ijazah`, `berkas_akte`, `published`, `updated`) VALUES
(1, '3512162345678989', 'hidayatus sofyan', 'Berkas/reg_lfDhvhR.png', 'Berkas/reg_yRe2xKq_8ozdbYT.png', 'Berkas/reg_dTErouq_RFFhm7P.png', '2023-08-18 17:22:57.965576', '2023-08-18 17:22:57.965576');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_guru`
--

CREATE TABLE `model_guru` (
  `id` bigint(20) NOT NULL,
  `nidn` varchar(25) NOT NULL,
  `nama` varchar(2000) NOT NULL,
  `alamat` varchar(2000) NOT NULL,
  `tempat_lahir` varchar(2000) NOT NULL,
  `jk` varchar(25) NOT NULL,
  `nohp` varchar(15) NOT NULL,
  `jabatan` varchar(250) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_guru`
--

INSERT INTO `model_guru` (`id`, `nidn`, `nama`, `alamat`, `tempat_lahir`, `jk`, `nohp`, `jabatan`, `foto`, `published`, `updated`) VALUES
(1, '089801', 'Drs. Matrawi, M.Pd', 'Kotaanyar', 'probolinggo', 'Laki-Laki', '085259701893', 'Kepala Sekolah', 'Berkas/icon_5f4ORlf.png', '2023-06-29 16:14:31.312044', '2023-06-29 16:15:43.073349'),
(2, '089802', 'Uswatun Hasanah, S.P', 'Kotaanyar', 'probolinggo', 'Perempuan', '085259701532', 'Waka Kurikulum', 'Berkas/icon_7qfq9PL_E1SqhkM.png', '2023-06-29 16:16:28.949883', '2023-06-29 16:16:28.949883'),
(3, '089803', 'Trisnani Dwi Lestari, S.Pd', 'sumberanyar', 'probolinggo', 'Perempuan', '085259701156', 'Waka Kesiswaan', 'Berkas/icon_7qfq9PL_BLs8wpE_XiOI5lZ_yRDGAgc.png', '2023-06-29 16:17:24.371542', '2023-06-29 16:17:24.371542'),
(4, '089804', 'Lukman Hakim, ST', 'Kotaanyar', 'probolinggo', 'Laki-Laki', '082334556889', 'Kepala Tata Usaha', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN.png', '2023-06-29 16:18:13.736315', '2023-06-29 16:18:13.736315'),
(5, '089805', 'Abdullah Qodir Audah, S.Pd', 'pakuniran', 'probolinggo', 'Laki-Laki', '085490290392', 'Bendahara', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_voWBcHk.png', '2023-06-29 16:19:33.244176', '2023-06-29 16:19:33.244176'),
(6, '089806', 'Ahmad Tijani, S.Kom', 'binor', 'probolinggo', 'Laki-Laki', '085259701532', 'Waka Sarpas', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_qoiiY8C.png', '2023-06-29 16:20:25.917404', '2023-06-29 16:20:25.917404'),
(7, '089807', 'Durroh Asyiqoh S. Pd', 'morong', 'probolinggo', 'Perempuan', '085259701156', 'Wali Kelas', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_Trp2AQH.png', '2023-06-29 16:21:31.769313', '2023-06-29 16:21:31.769313'),
(8, '089808', 'Yulie Ekawati, S.Pd', 'paiton', 'probolinggo', 'Perempuan', '082334556889', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_hyknarG.png', '2023-06-29 16:22:27.994706', '2023-06-29 16:22:27.994706'),
(9, '089809', 'Nur Sofi, S.Pd', 'Kotaanyar', 'probolinggo', 'Perempuan', '085490290392', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_ETrf9rD.png', '2023-06-29 16:23:20.172522', '2023-06-29 16:23:20.172522'),
(10, '089810', 'Naning Maftukhah, S.Pd', 'sumberanyar', 'probolinggo', 'Perempuan', '081867675656', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_8BnI5ff.png', '2023-06-29 16:24:12.836960', '2023-06-29 16:24:12.836960'),
(11, '089811', 'Sulusiyah, S.Pd', 'paiton', 'probolinggo', 'Perempuan', '085490290392', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_x8NsNi6.png', '2023-06-29 16:25:00.512516', '2023-06-29 16:25:00.512516'),
(12, '089812', 'Decky Abdi Dermawan, S.Par', 'Kotaanyar', 'probolinggo', 'Laki-Laki', '085490290392', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_g7BcMwh.png', '2023-06-29 16:25:41.896779', '2023-06-29 16:25:41.896779'),
(13, '089813', 'Masrofiq, S.Pd', 'sumberanyar', 'probolinggo', 'Laki-Laki', '085259701893', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_9wW2i4R.png', '2023-06-29 16:26:30.014795', '2023-06-29 16:26:30.014795'),
(14, '089814', 'Lia Andriani, S.Pd', 'Kotaanyar', 'probolinggo', 'Perempuan', '085259701156', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_Wcig0TN_Lb1T8O1.png', '2023-06-29 16:27:04.134359', '2023-06-29 16:27:04.134359'),
(15, '089815', 'Dainty Resy Suciati, S.Pd', 'sumberanyar', 'probolinggo', 'Perempuan', '085259701532', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_FkVgtw8.png', '2023-06-29 16:27:52.829368', '2023-06-29 16:27:52.829368'),
(16, '089816', 'Marisa Marta\'ati, S.Pd', 'paiton', 'probolinggo', 'Perempuan', '085259701156', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_FkVgtw8_K685xW8.png', '2023-06-29 16:28:33.955260', '2023-06-29 16:28:33.955260'),
(17, '089817', 'Nur Kistin Kamalia, S.Psi', 'paiton', 'probolinggo', 'Perempuan', '085259701156', 'Guru', 'Berkas/icon_5f4ORlf_KTnLePz.png', '2023-06-29 16:29:06.369422', '2023-06-29 16:29:06.369422'),
(18, '089818', 'M. Royyan S, S.Pd', 'binor', 'probolinggo', 'Laki-Laki', '085490290392', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_3EZMecW_f3gxy0J.png', '2023-06-29 16:29:55.924613', '2023-06-29 16:29:55.924613'),
(19, '089819', 'Nurul Mutowi\'ah, S.Si, M.pd', 'paiton', 'probolinggo', 'Perempuan', '085259701532', 'Guru', 'Berkas/icon_3kLhnl9_ctfy4Xe.png', '2023-06-29 16:30:39.645095', '2023-06-29 16:30:39.645095'),
(20, '089820', 'Ramadita Riyanto, S.Pd', 'Kotaanyar', 'probolinggo', 'Laki-Laki', '082334556889', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_2QJZaFg.png', '2023-06-29 16:31:42.818274', '2023-06-29 16:31:42.818274'),
(21, '089821', 'Kartiningsih, S.Pd', 'sumberanyar', 'probolinggo', 'Perempuan', '085490290392', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_l0dyjte.png', '2023-06-29 16:32:19.301708', '2023-06-29 16:32:19.301708'),
(22, '089822', 'Miftahul Huda', 'paiton', 'probolinggo', 'Laki-Laki', '085259701532', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_veEa9Ta.png', '2023-06-29 16:32:57.400041', '2023-06-29 16:32:57.400041'),
(23, '089823', 'Furqoni Syahfitri, S.Pd', 'Kotaanyar', 'probolinggo', 'Perempuan', '085259701532', 'Guru', 'Berkas/icon_7qfq9PL_BLs8wpE_TOPopt3.png', '2023-06-29 16:33:34.229685', '2023-06-29 16:33:34.229685'),
(24, '089824', 'Ma\'rufah, S.Pd', 'paiton', 'probolinggo', 'Laki-Laki', '085259701532', 'Guru Tahfidz', 'Berkas/icon_7qfq9PL_BLs8wpE_ZP5Q6Cd.png', '2023-06-29 16:34:26.770101', '2023-06-29 16:34:26.770101');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_jadwall1`
--

CREATE TABLE `model_jadwall1` (
  `id` bigint(20) NOT NULL,
  `nama_jadwal` varchar(1200) NOT NULL,
  `tanggal_jadwal` varchar(15) NOT NULL,
  `hari` varchar(25) NOT NULL,
  `nama_mapel` varchar(2000) NOT NULL,
  `kode_guru` varchar(1) NOT NULL,
  `nama_guru` varchar(2000) NOT NULL,
  `jurusan` varchar(2000) NOT NULL,
  `kelas` varchar(6) NOT NULL,
  `jam_mapel` varchar(12) NOT NULL,
  `jam_masuk` varchar(12) NOT NULL,
  `jam_istirahat` varchar(12) NOT NULL,
  `keterangan` varchar(2000) NOT NULL,
  `keterangan_jadwal` varchar(2000) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_jadwall1`
--

INSERT INTO `model_jadwall1` (`id`, `nama_jadwal`, `tanggal_jadwal`, `hari`, `nama_mapel`, `kode_guru`, `nama_guru`, `jurusan`, `kelas`, `jam_mapel`, `jam_masuk`, `jam_istirahat`, `keterangan`, `keterangan_jadwal`, `published`, `updated`) VALUES
(1, 'Jadwal Sekolah', '2023-08-07', 'Sabtu', 'Pendidikan Kewarganegaraan (PKN)', 'A', 'Drs. Matrawi, M.Pd', 'Tata Boga', 'X', 'Ke-1', '07 : 50', '09 : 50', 'Aktif', 'Semester Genap', '2023-08-07 12:24:44.056275', '2023-08-07 12:25:15.173783');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_jenis_pembayaran`
--

CREATE TABLE `model_jenis_pembayaran` (
  `id` bigint(20) NOT NULL,
  `jenis_pembayaran` varchar(1200) NOT NULL,
  `nominal` varchar(20) NOT NULL,
  `keterangan` varchar(1200) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_jenis_pembayaran`
--

INSERT INTO `model_jenis_pembayaran` (`id`, `jenis_pembayaran`, `nominal`, `keterangan`, `published`, `updated`) VALUES
(1, 'pendaftaran ', '150.000', 'pembayaran penerimaan peserta didik baru', '2023-08-18 17:00:38.989896', '2023-08-18 17:00:38.989896'),
(2, 'infaq syahriyah (SPP)', '250.000', 'pembayaran SPP', '2023-08-18 17:02:03.894103', '2023-08-18 17:02:03.894103');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_jurusan`
--

CREATE TABLE `model_jurusan` (
  `id` bigint(20) NOT NULL,
  `nama_jurusan` varchar(1200) NOT NULL,
  `keterangan` varchar(2000) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_jurusan`
--

INSERT INTO `model_jurusan` (`id`, `nama_jurusan`, `keterangan`, `published`, `updated`) VALUES
(1, 'Tata Boga', 'Aktif', '2023-06-23 17:07:51.206854', '2023-06-29 07:59:38.735453');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_kelas`
--

CREATE TABLE `model_kelas` (
  `id` bigint(20) NOT NULL,
  `nama_kelas` varchar(1200) NOT NULL,
  `kapasitas` varchar(20) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_kelas`
--

INSERT INTO `model_kelas` (`id`, `nama_kelas`, `kapasitas`, `published`, `updated`) VALUES
(1, 'X', '30', '2023-06-23 17:09:07.335907', '2023-07-09 04:16:34.428960'),
(2, 'XI', '30', '2023-06-23 17:09:17.507168', '2023-07-09 04:16:44.435015'),
(3, 'XII', '30', '2023-06-23 17:09:24.659423', '2023-07-09 04:16:52.352180');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_matapelajaran`
--

CREATE TABLE `model_matapelajaran` (
  `id` bigint(20) NOT NULL,
  `kode_mapel` varchar(25) NOT NULL,
  `nama_mapel` varchar(2000) NOT NULL,
  `keterangan` varchar(2000) NOT NULL,
  `kelompok_mapel` varchar(50) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_matapelajaran`
--

INSERT INTO `model_matapelajaran` (`id`, `kode_mapel`, `nama_mapel`, `keterangan`, `kelompok_mapel`, `published`, `updated`) VALUES
(1, '00001', 'PendidikanAgama Islam (PAI)', 'pembelajaran tentang pendidikan agama islam', 'A', '2023-06-29 18:03:01.815745', '2023-06-29 18:03:01.815745'),
(2, '00002', 'Pendidikan Kewarganegaraan (PKN)', 'pembelajaran tentang pendidikan kewarganegaraan ', 'A', '2023-06-29 18:05:53.604569', '2023-06-29 18:05:53.604569'),
(3, '00003', 'Bahasa Indonesia', 'pembelajaran tentang bhs indonesia', 'A', '2023-06-29 18:06:53.352482', '2023-06-29 18:06:53.352482'),
(4, '00004', 'Matematika', 'pembelajaran tentang Matematika', 'A', '2023-06-29 18:11:08.422224', '2023-06-29 18:11:08.422224'),
(5, '00005', 'Bahasa Inggris', 'pembelajaran tentang bhs inggris', 'A', '2023-06-29 18:11:42.959190', '2023-06-29 18:11:42.959190'),
(6, '00006', 'Sejarah Indonesia', 'pembelajaran tentang sejarah indonesia', 'A', '2023-06-29 18:12:36.166346', '2023-06-29 18:12:36.166346'),
(7, '00007', 'kepariwisataan', 'pembelajaran tentang kepariwisataan', 'A', '2023-06-29 18:13:09.900824', '2023-06-29 18:13:09.900824'),
(8, '00008', 'Keamanan Pangan', 'pembelajaran tentang keamanan pangan', 'A', '2023-06-29 18:13:58.057317', '2023-06-29 18:13:58.057317'),
(9, '00009', 'Pangan Bahan Makanan', 'pembelajaran tentang pangan bahan makanan', 'A', '2023-06-29 18:14:44.447050', '2023-06-29 18:14:44.447050'),
(10, '00010', 'Seni Budaya', 'pembelajaran tentang seni budaya', 'B', '2023-06-29 18:15:53.676427', '2023-06-29 18:15:53.676427'),
(11, '00011', 'Pendidikan Jasmani, Olahraga, dan Kesehatan (PJOK)', 'pembelajaran tentang PJOK', 'B', '2023-06-29 18:16:42.592544', '2023-06-29 18:16:42.592544'),
(12, '00012', 'Siskomdig (simulasi dan komunikasi digital)', 'pembelajaran tentang siskomdig', 'B', '2023-06-29 18:17:46.750682', '2023-06-29 18:19:45.500653'),
(13, '00013', 'Ipa Terapan', 'pembelajaran tentang ipa terapan', 'B', '2023-06-29 18:18:32.104630', '2023-06-29 18:20:24.466195'),
(14, '00014', 'Boga Dasar', 'pembelajaran tentang dasar-dasar boga', 'B', '2023-06-29 18:18:32.120612', '2023-06-29 18:20:47.170328'),
(15, '00015', 'Desain Grafis', 'pembelajaran tentang desain grafis', 'B', '2023-06-29 18:21:32.004392', '2023-06-29 18:21:32.004392'),
(16, '00016', 'Tata Hidang', 'pembelajaran tentang tata hidang', 'B', '2023-06-29 18:21:32.060409', '2023-06-29 18:23:02.221446'),
(17, '00017', 'Ilmu Gizi', 'pembelajaran tentang ilmu gizi', 'B', '2023-06-29 18:23:48.759575', '2023-06-29 18:23:48.759575'),
(18, '00018', 'Peng. dan Penyajian Makanan', 'pembelajaran tentang peng. dan penyajian makanan', 'B', '2023-06-29 18:25:04.684812', '2023-06-29 18:25:04.684812'),
(19, '00019', 'Produk Cake&Kue Indonesia', 'pembelajaran tentang produk cake dan kue indonesia', 'C', '2023-06-29 18:26:52.030037', '2023-06-29 18:26:52.030037'),
(20, '00020', 'Produk Pastry and Bakery', 'pembelajaran tentang pastry dan bakery', 'C', '2023-06-29 18:28:09.801078', '2023-06-29 18:28:09.801078'),
(21, '00021', 'Produk Kreatif dan Kewirausahaan', 'pembelajaran tentang produk kreatif dan kewirausahaan', 'C', '2023-06-29 18:29:41.911029', '2023-06-29 18:29:41.911029'),
(22, '00022', 'English Corversation Club', 'pembelajaran tentang english conversation club', 'C', '2023-06-29 18:30:47.914435', '2023-06-29 18:30:47.914435'),
(23, '00023', 'Design Produk', 'pembelajaran tentang design produk', 'C', '2023-06-29 18:31:50.681033', '2023-06-29 18:31:50.681033'),
(24, '00024', 'Karya Cipta Produk', 'pembelajaran tentang karya cipta produk', 'C', '2023-06-29 18:33:03.147406', '2023-06-29 18:33:03.147406'),
(25, '00025', 'Bahasa Arab', 'pembelajaran tentang bhs arab', 'Mulok', '2023-06-29 18:34:00.779884', '2023-06-29 18:34:00.779884'),
(26, '00026', 'LEMBAGA PENDIDIKAN AL-QUR\'AN (LPQ)', 'pembelajaran tentang LPQ', 'Mulok', '2023-06-29 18:35:05.296624', '2023-06-29 18:35:05.296624'),
(27, '00027', 'Pramuka', 'pembelajaran tentang pramuka', 'Mulok', '2023-06-29 18:35:52.785895', '2023-06-29 18:35:52.785895'),
(28, '00028', 'Kelompok Ilmiah Remaja', 'pembelajaran tentang kelompok ilmiah remaja', 'Mulok', '2023-06-29 18:37:12.430357', '2023-06-29 18:37:12.430357');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_nilairapot`
--

CREATE TABLE `model_nilairapot` (
  `id` bigint(20) NOT NULL,
  `nama_siswa` varchar(1200) NOT NULL,
  `no_induk` varchar(11) NOT NULL,
  `nama_kelas` varchar(12) NOT NULL,
  `nama_jurusan` varchar(1200) NOT NULL,
  `nama_mapel` varchar(1200) NOT NULL,
  `kelompok_mapel` varchar(1200) NOT NULL,
  `nilai_pengetahuan` varchar(12) NOT NULL,
  `deskripsi_pengetahuan` varchar(1200) NOT NULL,
  `nilai_keterampilan` varchar(12) NOT NULL,
  `deskripsi_keterampilan` varchar(1200) NOT NULL,
  `nilai_kkm` varchar(12) NOT NULL,
  `jumlah_nilai` varchar(12) NOT NULL,
  `rata_rata` varchar(12) NOT NULL,
  `kegiatan_ekstra` varchar(1200) NOT NULL,
  `keterangan_esktra` varchar(1200) NOT NULL,
  `prestasi` varchar(1200) NOT NULL,
  `keterangan_prestasi` varchar(1200) NOT NULL,
  `jml_sakit` varchar(12) NOT NULL,
  `jml_izin` varchar(12) NOT NULL,
  `tanpa_keterangan` varchar(12) NOT NULL,
  `keterangan_raport` varchar(1200) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_nilairapot`
--

INSERT INTO `model_nilairapot` (`id`, `nama_siswa`, `no_induk`, `nama_kelas`, `nama_jurusan`, `nama_mapel`, `kelompok_mapel`, `nilai_pengetahuan`, `deskripsi_pengetahuan`, `nilai_keterampilan`, `deskripsi_keterampilan`, `nilai_kkm`, `jumlah_nilai`, `rata_rata`, `kegiatan_ekstra`, `keterangan_esktra`, `prestasi`, `keterangan_prestasi`, `jml_sakit`, `jml_izin`, `tanpa_keterangan`, `keterangan_raport`, `published`, `updated`) VALUES
(1, 'ANGEL GIAN PUTRI', '001/001.119', 'XI', 'Tata Boga', 'PendidikanAgama Islam (PAI)', 'A', '80', 'Siswa Dapat menerapkan fungsi sosial, struktur teks, dan unsur kebahasaan teks transaksional lisan dan tulis yang melibatkan tindakan memberi dan meminta informasi terkait jati diri.', '80', 'Siswa Dapat menginterpretasi isi teks laporan hasil observasi berdasarkan intrepretasi baik secara lisan maupun tulisan, mengonstrukturkan teks laporan hasil observasi dengan.', '75', '160', '80', 'pramuka', 'terbaik', '1', 'iya', '0', '0', '0', 'XII (Dua Belas)', '2023-08-11 15:25:35.720265', '2023-08-11 15:49:08.829444');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_nilai_tes`
--

CREATE TABLE `model_nilai_tes` (
  `id` bigint(20) NOT NULL,
  `no_ktp` varchar(1200) NOT NULL,
  `nama_lengkap` varchar(1200) NOT NULL,
  `jumlah_nilai` varchar(1200) NOT NULL,
  `rata_nilai` varchar(1200) NOT NULL,
  `tanggal_tes` varchar(1200) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_nilai_tes`
--

INSERT INTO `model_nilai_tes` (`id`, `no_ktp`, `nama_lengkap`, `jumlah_nilai`, `rata_nilai`, `tanggal_tes`, `published`, `updated`) VALUES
(1, '3512162345678989', 'hidayatus sofyan', '50', '45.5', '19-08-2023', '2023-08-18 17:25:21.584602', '2023-08-18 17:25:21.584602'),
(2, '3512162345678989', 'hidayatus sofyan', '50', '45.5', '19-08-2023', '2023-08-18 17:26:22.757061', '2023-08-18 17:26:22.757061');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_pembayaran_manajemen`
--

CREATE TABLE `model_pembayaran_manajemen` (
  `id` bigint(20) NOT NULL,
  `nis` varchar(20) NOT NULL,
  `nama_siswa` varchar(20) NOT NULL,
  `kelas` varchar(20) NOT NULL,
  `jurusan` varchar(20) NOT NULL,
  `jenis_pembayaran` varchar(1200) NOT NULL,
  `total` varchar(120) NOT NULL,
  `nominal` varchar(20) NOT NULL,
  `jumlah_tanggungan` varchar(20) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `tahun_akademik` varchar(20) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_pembayaran_manajemen`
--

INSERT INTO `model_pembayaran_manajemen` (`id`, `nis`, `nama_siswa`, `kelas`, `jurusan`, `jenis_pembayaran`, `total`, `nominal`, `jumlah_tanggungan`, `semester`, `tahun_akademik`, `published`, `updated`) VALUES
(1, '001/001.119', 'ANGEL GIAN PUTRI', 'XI', 'Tata Boga', 'pendaftaran ', '150', '100', '-50', 'Semester 1', '2023', '2023-08-18 17:03:35.370312', '2023-08-18 17:03:35.371306'),
(2, '001/001.119', 'ANGEL GIAN PUTRI', 'XI', 'Tata Boga', 'infaq syahriyah (SPP)', '250', '250', '0', 'Semester 1', '2023', '2023-08-18 17:04:37.316570', '2023-08-18 17:04:37.316570');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_pendaftaran_pesertappdb`
--

CREATE TABLE `model_pendaftaran_pesertappdb` (
  `id` bigint(20) NOT NULL,
  `no_kk` varchar(16) NOT NULL,
  `no_ktp` varchar(16) NOT NULL,
  `nama_lengkap` varchar(1200) NOT NULL,
  `alamat` varchar(1200) NOT NULL,
  `jk` varchar(25) NOT NULL,
  `tempat_lahir` varchar(1200) NOT NULL,
  `tanggal_lahir` varchar(25) NOT NULL,
  `nohp` varchar(15) NOT NULL,
  `email` varchar(1200) NOT NULL,
  `pendidikan_akhir` varchar(1200) NOT NULL,
  `nama_ibu` varchar(1200) NOT NULL,
  `nama_ayah` varchar(1200) NOT NULL,
  `pekerjaan_ibu` varchar(1200) NOT NULL,
  `pekerjaan_ayah` varchar(1200) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `nama_jurusan` varchar(1200) NOT NULL,
  `status_penerimaan` varchar(1200) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_pendaftaran_pesertappdb`
--

INSERT INTO `model_pendaftaran_pesertappdb` (`id`, `no_kk`, `no_ktp`, `nama_lengkap`, `alamat`, `jk`, `tempat_lahir`, `tanggal_lahir`, `nohp`, `email`, `pendidikan_akhir`, `nama_ibu`, `nama_ayah`, `pekerjaan_ibu`, `pekerjaan_ayah`, `foto`, `nama_jurusan`, `status_penerimaan`, `published`, `updated`) VALUES
(1, '3512163746528264', '3512162345678989', 'hidayatus sofyan', 'besuki', 'Laki-Laki', 'SITUBONDO', '2000-09-09', '+6285234833259', 'sofyan@gmail.com', 'smp islam paiton', 'ibunda', 'ayahhanda', 'mengurus rumah tangga', 'petani', 'Berkas/06_wWSbl7m.jpg', 'Tata Boga', 'Di Terima', '2023-08-18 17:22:23.149500', '2023-08-18 17:48:45.340589');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_peringkat`
--

CREATE TABLE `model_peringkat` (
  `id` bigint(20) NOT NULL,
  `no_induk` varchar(1200) NOT NULL,
  `nama_siswa` varchar(2000) NOT NULL,
  `kelas` varchar(2000) NOT NULL,
  `jurusan` varchar(2000) NOT NULL,
  `nilai_raport` varchar(2000) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_ppdb`
--

CREATE TABLE `model_ppdb` (
  `id` bigint(20) NOT NULL,
  `no_ktp` varchar(16) NOT NULL,
  `nama_lengkap` varchar(1200) NOT NULL,
  `alamat` varchar(1200) NOT NULL,
  `jk` varchar(25) NOT NULL,
  `nohp` varchar(25) NOT NULL,
  `username` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_ppdb`
--

INSERT INTO `model_ppdb` (`id`, `no_ktp`, `nama_lengkap`, `alamat`, `jk`, `nohp`, `username`, `password`, `published`, `updated`) VALUES
(1, '3512162345678989', 'hidayatus sofyan', 'besuki', 'Laki-Laki', '085234833259', 'sofyan', 'sofyan123', '2023-08-18 17:19:12.066491', '2023-08-18 17:19:12.066491');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_siswa1`
--

CREATE TABLE `model_siswa1` (
  `id` bigint(20) NOT NULL,
  `nis` varchar(1200) NOT NULL,
  `nama_lengkap` varchar(1200) NOT NULL,
  `jk` varchar(25) NOT NULL,
  `alamat` varchar(1250) NOT NULL,
  `tempat_lahir` varchar(12000) NOT NULL,
  `tanggal_lahir` varchar(25) NOT NULL,
  `nohp` varchar(25) NOT NULL,
  `jurusan` varchar(250) NOT NULL,
  `kelas` varchar(50) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `tahun_masuk` varchar(50) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_siswa1`
--

INSERT INTO `model_siswa1` (`id`, `nis`, `nama_lengkap`, `jk`, `alamat`, `tempat_lahir`, `tanggal_lahir`, `nohp`, `jurusan`, `kelas`, `foto`, `tahun_masuk`, `published`, `updated`) VALUES
(2, '001/001.119', 'ANGEL GIAN PUTRI', 'Perempuan', 'besuki', 'Situbondo', '2016-06-07', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_08ROT6F.jpg', '2018', '2023-06-29 16:44:12.856298', '2023-08-07 12:10:05.307221'),
(3, '002/002.119', 'ANISA PRATAMA PUTRI', 'Perempuan', 'paiton', 'probolinggo', '2016-01-09', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_E4MWLOy.jpg', '', '2023-06-29 16:45:38.225819', '2023-07-09 04:25:22.832801'),
(4, '003/003.119', 'DIMAS ANDRIAN', 'Laki-Laki', 'paiton', 'probolinggo', '2016-02-26', '085490290392', 'Tata Boga', 'XI', 'Berkas/06_QQZAPJE.jpg', '', '2023-06-29 16:46:39.004106', '2023-07-09 04:25:34.701615'),
(5, '004/004.119', 'FARADISA MAGHFIROH', 'Perempuan', 'binor', 'probolinggo', '2016-06-08', '086867675656', 'Tata Boga', 'XI', 'Berkas/06_IO97V3K.jpg', '', '2023-06-29 16:48:13.155901', '2023-07-09 04:25:46.029039'),
(6, '005/005.119', 'FATIHATUN NABILA', 'Perempuan', 'Kotaanyar', 'probolinggo', '2016-06-21', '085259701532', 'Tata Boga', 'XI', 'Berkas/06_fFl8n4e.jpg', '', '2023-06-29 16:49:13.853501', '2023-07-09 04:25:59.271239'),
(7, '006/006.119', 'HALIMATUS SA’DIYAH', 'Perempuan', 'sumberanyar', 'probolinggo', '2016-03-16', '085490290392', 'Tata Boga', 'XI', 'Berkas/06_IyCBigF.jpg', '', '2023-06-29 16:50:50.464913', '2023-07-09 04:34:20.964770'),
(8, '007/007.119', 'INDIANA SAFITRI', 'Perempuan', 'paiton', 'probolinggo', '2016-10-25', '085259701532', 'Tata Boga', 'XI', 'Berkas/06_aajjsPM.jpg', '', '2023-06-29 16:52:38.650712', '2023-07-09 04:34:36.165229'),
(9, '008/008.119', 'INDRI FITRIANI MARHAMAH', 'Perempuan', 'binor', 'probolinggo', '2016-06-07', '082334556889', 'Tata Boga', 'XI', 'Berkas/06_GgLfs23.jpg', '', '2023-06-29 16:53:45.271812', '2023-07-09 04:34:48.202712'),
(10, '009/009.119', 'INDRI YANI', 'Perempuan', 'Kotaanyar', 'probolinggo', '2016-11-29', '085490290392', 'Tata Boga', 'XI', 'Berkas/06_LsSrocu.jpg', '', '2023-06-29 16:54:53.050379', '2023-07-09 04:34:59.589077'),
(11, '010/010.119', 'JANNATUL FIRDAUSIAH', 'Perempuan', 'besuki', 'Situbondo', '2016-01-14', '085259701532', 'Tata Boga', 'XI', 'Berkas/06_80lqVtT.jpg', '', '2023-06-29 16:55:51.351400', '2023-07-09 04:35:14.134216'),
(12, '011/011.119', 'LAILATUL MUKARROMAH', 'Perempuan', 'paiton', 'probolinggo', '2016-10-29', '086867675656', 'Tata Boga', 'XI', 'Berkas/06_WXm51Gy.jpg', '', '2023-06-29 16:57:28.728015', '2023-07-09 04:36:49.591828'),
(13, '012/012.119', 'MOH.NOR SYAIFUDDIN', 'Laki-Laki', 'Kotaanyar', 'probolinggo', '2016-05-15', '085259701156', 'Tata Boga', 'XI', 'Berkas/06_EbYXzoy.jpg', '', '2023-06-29 16:58:25.448540', '2023-07-09 04:37:20.442075'),
(14, '013/013.119', 'NADYA RAFILA KAMILA', 'Perempuan', 'besuki', 'Situbondo', '2016-07-23', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_3dOeAVx.jpg', '', '2023-06-29 16:59:33.474450', '2023-07-09 04:37:36.910696'),
(15, '014/014.119', 'NAFILA RIZQIYAH', 'Perempuan', 'binor', 'probolinggo', '2016-11-09', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_qfbTjJ9.jpg', '', '2023-06-29 17:00:38.392247', '2023-07-09 04:37:51.672583'),
(16, '015/015.119', 'NAILUL HIDAYAH', 'Perempuan', 'binor', 'probolinggo', '2016-11-09', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_4hc9RtQ.jpg', '', '2023-06-29 17:02:22.318084', '2023-07-09 04:37:06.349258'),
(17, '016/016.119', 'ROVALINA PUTRI ADELIA', 'Perempuan', 'besuki', 'Situbondo', '2016-09-29', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_AxdvHqh.jpg', '', '2023-06-29 17:03:21.702495', '2023-07-09 04:36:32.448470'),
(18, '017/017.119', 'SITI RODIAH', 'Perempuan', 'Kotaanyar', 'probolinggo', '2016-10-30', '085490290392', 'Tata Boga', 'XI', 'Berkas/06_CF6cLfo.jpg', '', '2023-06-29 17:04:23.217572', '2023-07-09 04:36:15.495368'),
(19, '018/018.119', 'ULFA MAGHFIROH', 'Perempuan', 'besuki', 'Situbondo', '2016-12-30', '085259701893', 'Tata Boga', 'XI', 'Berkas/06_6zwmF2R.jpg', '', '2023-06-29 17:05:22.259354', '2023-07-09 04:35:43.861253'),
(20, '019/019.119', 'ARIL SAPUTTRA', 'Laki-Laki', 'sumberanyar', 'probolinggo', '2016-02-29', '082334556889', 'Tata Boga', 'XI', 'Berkas/06_ZrbyvY3.jpg', '', '2023-06-29 17:06:18.900882', '2023-07-09 04:35:29.024620'),
(21, '020/020.119', 'ABDUL ARUSIN', 'Laki-Laki', 'paiton', 'probolinggo', '2020-02-04', '086867675656', 'Tata Boga', 'X', 'Berkas/06_iFLbk8v.jpg', '', '2023-06-29 17:14:38.808403', '2023-07-09 04:35:57.984751'),
(22, '021/021.119', 'AGUS SATRIYO', 'Laki-Laki', 'besuki', 'Situbondo', '2020-02-15', '085259701893', 'Tata Boga', 'X', 'Berkas/06_pyURVaj.jpg', '', '2023-06-29 17:15:51.384222', '2023-07-09 04:40:53.739704'),
(23, '022/022.119', 'AHAMAD SUGIONO', 'Laki-Laki', 'Kotaanyar', 'probolinggo', '2020-01-30', '085490290392', 'Tata Boga', 'X', 'Berkas/06_dnELpIK.jpg', '', '2023-06-29 17:16:59.725110', '2023-07-09 04:40:37.794155'),
(24, '023/023.119', 'AMINATUL MUFIDAH AZIZI', 'Perempuan', 'paiton', 'probolinggo', '2020-09-23', '085259701156', 'Tata Boga', 'X', 'Berkas/06_dnlSGSM.jpg', '', '2023-06-29 17:17:57.337411', '2023-07-09 04:40:18.377360'),
(25, '024/024.119', 'FIRDAUS YATUL JANNAH', 'Perempuan', 'sumberanyar', 'probolinggo', '2020-02-29', '085259701156', 'Tata Boga', 'X', 'Berkas/06_8RnOysG.jpg', '', '2023-06-29 17:19:01.983279', '2023-07-09 04:40:02.336707'),
(26, '025/025.119', 'HALIMATUL HOSNA', 'Perempuan', 'sumberanyar', 'probolinggo', '2020-06-21', '082334556889', 'Tata Boga', 'X', 'Berkas/06_9i8oTHn.jpg', '', '2023-06-29 17:19:53.674223', '2023-07-09 04:39:45.714020'),
(27, '026/026.119', 'HARYONO', 'Laki-Laki', 'binor', 'probolinggo', '2020-08-17', '085490290392', 'Tata Boga', 'X', 'Berkas/06_sbZoGk3.jpg', '', '2023-06-29 17:35:57.012451', '2023-07-09 04:39:29.417303'),
(28, '027/027.119', 'HOTIMATUL HOSNA', 'Perempuan', 'paiton', 'probolinggo', '2020-06-16', '082334556889', 'Tata Boga', 'X', 'Berkas/06_CIIZVW2.jpg', '', '2023-06-29 17:36:49.944358', '2023-07-09 04:39:12.692518'),
(29, '028/028.119', 'HUWAIDA FINA DZAKIYAH', 'Perempuan', 'sumberanyar', 'probolinggo', '2020-06-30', '085259701893', 'Tata Boga', 'X', 'Berkas/06_mGnknjU.jpg', '', '2023-06-29 17:37:44.439009', '2023-07-09 04:38:55.740144'),
(30, '029/029.119', 'ICHA WIDIAWATI', 'Perempuan', 'besuki', 'Situbondo', '2020-04-30', '085259701893', 'Tata Boga', 'X', 'Berkas/06_xz9Zv3J.jpg', '', '2023-06-29 17:38:47.758668', '2023-07-09 04:38:39.769877'),
(31, '030/030.119', 'JAMILA CANDRA', 'Laki-Laki', 'paiton', 'probolinggo', '2020-06-30', '085490290392', 'Tata Boga', 'X', 'Berkas/06_E21l36j.jpg', '', '2023-06-29 17:39:41.789242', '2023-07-09 04:38:16.668272'),
(32, '031/031.119', 'KURATUN NISA\'', 'Perempuan', 'besuki', 'Situbondo', '2020-08-09', '085259701893', 'Tata Boga', 'X', 'Berkas/06_Z78qr3U.jpg', '', '2023-06-29 17:40:38.039392', '2023-07-09 04:43:45.396541'),
(33, '032/032.119', 'LATIFA CANDRA', 'Perempuan', 'sumberanyar', 'probolinggo', '2020-10-30', '085490290392', 'Tata Boga', 'X', 'Berkas/06_BcbZX8y.jpg', '', '2023-06-29 17:41:48.742083', '2023-07-09 04:43:28.059841'),
(34, '033/033.119', 'MARIA ULFA', 'Perempuan', 'besuki', 'Situbondo', '2020-07-09', '085259701156', 'Tata Boga', 'X', 'Berkas/06_I0m7eEY.jpg', '', '2023-06-29 17:42:40.604276', '2023-07-09 04:43:13.563420'),
(35, '034/034.119', 'NOVIA ANISWATUN R', 'Perempuan', 'batu gajah', 'probolinggo', '2020-06-30', '085259701156', 'Tata Boga', 'X', 'Berkas/06_rtdJo0L.jpg', '', '2023-06-29 17:43:56.904794', '2023-07-09 04:42:58.333705'),
(36, '035/035.119', 'NUR INDAH INDRIANI', 'Perempuan', 'kraksaan', 'probolinggo', '2020-09-16', '085259701893', 'Tata Boga', 'X', 'Berkas/06_gIbQdh4.jpg', '', '2023-06-29 17:44:53.826801', '2023-07-09 04:42:41.308842'),
(37, '036/036.119', 'NUR LAILATUL JANNAH', 'Perempuan', 'kraksaan', 'probolinggo', '2020-07-16', '085259701532', 'Tata Boga', 'X', 'Berkas/06_GVHcEAU.jpg', '', '2023-06-29 17:45:52.967226', '2023-07-09 04:42:24.571214'),
(38, '037/037.119', 'RIZKA NAZILA', 'Perempuan', 'batur', 'probolinggo', '2020-10-03', '085259701893', 'Tata Boga', 'X', 'Berkas/06_SXWo7oc.jpg', '', '2023-06-29 17:47:00.975623', '2023-07-09 04:42:10.151761'),
(39, '038/038.119', 'ROFIATUL HASANAH', 'Perempuan', 'binor', 'probolinggo', '2020-09-09', '085259701893', 'Tata Boga', 'X', 'Berkas/06_0FzDP4l.jpg', '', '2023-06-29 17:48:03.096018', '2023-07-09 04:41:56.752245'),
(40, '039/039.119', 'ROVIATUL JANNAH', 'Perempuan', 'binor', 'probolinggo', '2020-09-09', '085490290392', 'Tata Boga', 'X', 'Berkas/06_NToUkk2.jpg', '', '2023-06-29 17:48:56.793022', '2023-07-09 04:41:36.027206'),
(41, '040/040.119', 'RUNAEDAH', 'Perempuan', 'kraksaan', 'probolinggo', '2020-10-30', '085259701532', 'Tata Boga', 'X', 'Berkas/06_nhYonm4.jpg', '', '2023-06-29 17:49:57.638085', '2023-07-09 04:41:16.818296'),
(42, '041/041.119', 'ZAINUL', 'Laki-Laki', 'Kotaanyar', 'probolinggo', '2020-10-20', '085259701156', 'Tata Boga', 'X', 'Berkas/06_KSvqIF2.jpg', '', '2023-06-29 17:51:00.193496', '2023-07-09 04:44:04.475302');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_tahun_pelajaran`
--

CREATE TABLE `model_tahun_pelajaran` (
  `id` bigint(20) NOT NULL,
  `tahun` varchar(1200) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_tahun_pelajaran`
--

INSERT INTO `model_tahun_pelajaran` (`id`, `tahun`, `semester`, `published`, `updated`) VALUES
(1, '2023', 'Semester Genap', '2023-08-07 12:01:15.489895', '2023-08-07 12:01:15.489895'),
(2, '2023', 'Semester Ganjil', '2023-08-07 12:02:53.291130', '2023-08-07 12:02:53.291130'),
(3, '2023', 'Semester Akhir', '2023-08-07 12:03:03.121990', '2023-08-07 12:04:07.738315');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_tes_pesertadb1`
--

CREATE TABLE `model_tes_pesertadb1` (
  `id` bigint(20) NOT NULL,
  `no_ktp` varchar(1200) NOT NULL,
  `nama_lengkap` varchar(1200) NOT NULL,
  `nama_mapel` varchar(1200) NOT NULL,
  `soal_mapel` varchar(1200) NOT NULL,
  `jawaban` varchar(1200) NOT NULL,
  `tanggal_tes` varchar(1200) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_tes_pesertadb1`
--

INSERT INTO `model_tes_pesertadb1` (`id`, `no_ktp`, `nama_lengkap`, `nama_mapel`, `soal_mapel`, `jawaban`, `tanggal_tes`, `published`, `updated`) VALUES
(1, '3512162345678989', 'hidayatus sofyan', 'PendidikanAgama Islam (PAI)', 'Rukun Haji ada berjumlah…', '[\"Tawaf Wada\'\", \'6 macam\']', '19-08-2023', '2023-08-18 17:23:22.764207', '2023-08-18 17:23:22.764207'),
(2, '3512162345678989', 'hidayatus sofyan', 'PendidikanAgama Islam (PAI)', 'Rukun Haji ada berjumlah…', '[\"Tawaf Wada\'\", \'6 macam\']', '19-08-2023', '2023-08-18 17:23:22.816761', '2023-08-18 17:23:22.816761');

-- --------------------------------------------------------

--
-- Struktur dari tabel `model_tes_soalppdb`
--

CREATE TABLE `model_tes_soalppdb` (
  `id` bigint(20) NOT NULL,
  `nama_mapel` varchar(1200) NOT NULL,
  `soal_mapel` varchar(1200) NOT NULL,
  `nilai_mapel` varchar(1200) NOT NULL,
  `a` varchar(1200) NOT NULL,
  `b` varchar(1200) NOT NULL,
  `c` varchar(1200) NOT NULL,
  `d` varchar(1200) NOT NULL,
  `kunci_jawaban` varchar(1200) NOT NULL,
  `tanggal_tes` varchar(1200) NOT NULL,
  `published` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `model_tes_soalppdb`
--

INSERT INTO `model_tes_soalppdb` (`id`, `nama_mapel`, `soal_mapel`, `nilai_mapel`, `a`, `b`, `c`, `d`, `kunci_jawaban`, `tanggal_tes`, `published`, `updated`) VALUES
(1, 'PendidikanAgama Islam (PAI)', 'Tawaf yang dilakukan ketika akan meninggalkan kota Makkah disebut Tawaf ……', '50', 'Tawaf Ifadah', 'Tawaf Qudum', 'Tawaf Wada\'', 'Tawaf Sunnah', 'C', '2023-08-01', '2023-08-18 16:53:28.513835', '2023-08-18 16:53:28.513835'),
(2, 'PendidikanAgama Islam (PAI)', 'Rukun Haji ada berjumlah…', '50', '6 macam', '5 macam', '4 macam', '3 macam', 'A', '2023-08-01', '2023-08-18 16:55:57.230716', '2023-08-18 16:55:57.230716');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indeks untuk tabel `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indeks untuk tabel `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indeks untuk tabel `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indeks untuk tabel `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indeks untuk tabel `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indeks untuk tabel `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indeks untuk tabel `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indeks untuk tabel `model_berkasppdb`
--
ALTER TABLE `model_berkasppdb`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_guru`
--
ALTER TABLE `model_guru`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_jadwall1`
--
ALTER TABLE `model_jadwall1`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_jenis_pembayaran`
--
ALTER TABLE `model_jenis_pembayaran`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_jurusan`
--
ALTER TABLE `model_jurusan`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_kelas`
--
ALTER TABLE `model_kelas`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_matapelajaran`
--
ALTER TABLE `model_matapelajaran`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_nilairapot`
--
ALTER TABLE `model_nilairapot`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_nilai_tes`
--
ALTER TABLE `model_nilai_tes`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_pembayaran_manajemen`
--
ALTER TABLE `model_pembayaran_manajemen`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_pendaftaran_pesertappdb`
--
ALTER TABLE `model_pendaftaran_pesertappdb`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_peringkat`
--
ALTER TABLE `model_peringkat`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_ppdb`
--
ALTER TABLE `model_ppdb`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_siswa1`
--
ALTER TABLE `model_siswa1`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_tahun_pelajaran`
--
ALTER TABLE `model_tahun_pelajaran`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_tes_pesertadb1`
--
ALTER TABLE `model_tes_pesertadb1`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `model_tes_soalppdb`
--
ALTER TABLE `model_tes_soalppdb`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT untuk tabel `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT untuk tabel `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT untuk tabel `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT untuk tabel `model_berkasppdb`
--
ALTER TABLE `model_berkasppdb`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `model_guru`
--
ALTER TABLE `model_guru`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT untuk tabel `model_jadwall1`
--
ALTER TABLE `model_jadwall1`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `model_jenis_pembayaran`
--
ALTER TABLE `model_jenis_pembayaran`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `model_jurusan`
--
ALTER TABLE `model_jurusan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `model_kelas`
--
ALTER TABLE `model_kelas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `model_matapelajaran`
--
ALTER TABLE `model_matapelajaran`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT untuk tabel `model_nilairapot`
--
ALTER TABLE `model_nilairapot`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `model_nilai_tes`
--
ALTER TABLE `model_nilai_tes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `model_pembayaran_manajemen`
--
ALTER TABLE `model_pembayaran_manajemen`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `model_pendaftaran_pesertappdb`
--
ALTER TABLE `model_pendaftaran_pesertappdb`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `model_peringkat`
--
ALTER TABLE `model_peringkat`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `model_ppdb`
--
ALTER TABLE `model_ppdb`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `model_siswa1`
--
ALTER TABLE `model_siswa1`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT untuk tabel `model_tahun_pelajaran`
--
ALTER TABLE `model_tahun_pelajaran`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `model_tes_pesertadb1`
--
ALTER TABLE `model_tes_pesertadb1`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `model_tes_soalppdb`
--
ALTER TABLE `model_tes_soalppdb`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ketidakleluasaan untuk tabel `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ketidakleluasaan untuk tabel `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
