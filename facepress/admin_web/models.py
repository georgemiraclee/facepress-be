from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import signals

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email harus diisi')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dosen', 'Dosen'),
        ('mahasiswa', 'Mahasiswa'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email
    
class Admin(AbstractBaseUser):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, related_name='admin')  # Field untuk relasi dengan User
    nip = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nip', 'name']

    def __str__(self):
        return self.name

class Dosen(AbstractBaseUser):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, related_name='dosen')  # Field untuk relasi dengan User
    email = models.EmailField(unique=True)
    nip = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nip', 'nama']

    mata_kuliah = models.ManyToManyField('MataKuliah', through='MataKuliahDosen', related_name='dosens')

    def __str__(self):
        return self.nama

class Mahasiswa(AbstractBaseUser):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, related_name='mahasiswa')  # Field untuk relasi dengan User
    email = models.EmailField(unique=True)
    nim = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    semester = models.IntegerField()
    is_wajah_exist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    mobile_phone = models.CharField(max_length=20)
    nik = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nim', 'nama']

    mata_kuliah = models.ManyToManyField('MataKuliah', through='MataKuliahMahasiswa', related_name='mahasiswas')
    kelas = models.ManyToManyField('Kelas', through='MataKuliahMahasiswa', related_name='mahasiswas')
    jadwal = models.ManyToManyField('JadwalKelas', through='PresensiMahasiswa', related_name='mahasiswas')

    def __str__(self):
        return self.nama

class MataKuliah(models.Model):
    nama = models.CharField(max_length=255)
    nama_english = models.CharField(max_length=255, blank=True, null=True)
    kode = models.CharField(max_length=255, unique=True)
    tipe = models.CharField(max_length=255)
    sks = models.IntegerField()
    semester = models.IntegerField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.nama

class MataKuliahDosen(models.Model):
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE)
    dosen = models.ForeignKey('Dosen', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mata_kuliah.nama} - {self.dosen.nama}"

class MataKuliahMahasiswa(models.Model):
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE)
    mahasiswa = models.ForeignKey('Mahasiswa', on_delete=models.CASCADE)
    kelas = models.ForeignKey('Kelas', on_delete=models.CASCADE)
    semester_mengambil = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.mata_kuliah.nama} - {self.kelas.nama_kelas}"

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=255)
    kode_kelas = models.CharField(max_length=255, unique=True)
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE, related_name='kelas')
    ruang = models.ForeignKey('Ruang', on_delete=models.CASCADE, related_name='kelas')
    hari = models.CharField(max_length=255)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    kapasitas = models.IntegerField()

    def __str__(self):
        return self.nama_kelas

class Ruang(models.Model):
    nama_ruang = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_ruang

class JadwalKelas(models.Model):
    tanggal = models.DateField()
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE, related_name='jadwal_kelas')
    kelas = models.ForeignKey('Kelas', on_delete=models.CASCADE, related_name='jadwal_kelas')
    ruang = models.ForeignKey('Ruang', on_delete=models.CASCADE, related_name='jadwal_kelas')
    dosen = models.ForeignKey('Dosen', on_delete=models.CASCADE, related_name='jadwal_kelas')
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.mata_kuliah.nama} - {self.tanggal}"

def mata_kuliah_pre_delete(sender, instance, **kwargs):
    MataKuliahMahasiswa.objects.filter(mata_kuliah=instance).delete()
    MataKuliahDosen.objects.filter(mata_kuliah=instance).delete()
    JadwalKelas.objects.filter(mata_kuliah=instance).delete()
    Kelas.objects.filter(mata_kuliah=instance).delete()

signals.pre_delete.connect(mata_kuliah_pre_delete, sender=MataKuliah)

class PresensiMahasiswa(models.Model):
    STATUS_CHOICES = [
        ('hadir', 'Hadir'),
        ('alpha', 'Alpha'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
    ]

    mahasiswa = models.ForeignKey('Mahasiswa', on_delete=models.CASCADE)
    mata_kuliah = models.ForeignKey('MataKuliah', on_delete=models.CASCADE)
    kelas = models.ForeignKey('Kelas', on_delete=models.CASCADE)
    jadwal_kelas = models.ForeignKey('JadwalKelas', on_delete=models.CASCADE, related_name='presensi')  # Tambahkan related_name
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)  # Allow null
    presensi_oleh = models.CharField(max_length=100, null=True, blank=True)  # Allow null
    tanggal_presensi = models.DateField(null=True, blank=True)  # Allow null

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.tanggal_presensi}"


class FaceDataset(models.Model):
    mahasiswa = models.ForeignKey('Mahasiswa', on_delete=models.CASCADE, related_name='face_datasets')
    image_1 = models.ImageField(upload_to='face_datasets/')
    image_2 = models.ImageField(upload_to='face_datasets/')
    image_3 = models.ImageField(upload_to='face_datasets/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dataset Wajah - {self.mahasiswa.nama}"
    
class WajahMahasiswa(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='wajah')
    image = models.ImageField(upload_to='wajah_mahasiswa/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wajah {self.mahasiswa.nama} - {self.created_at}"