<body>
    <h1>README - Setup Django Rest Framework</h1>
    <ol>
        <li>Clone repository:
            <pre>git clone https://github.com/samuelpermana/facepressBE.git</pre>
        </li>
        <li>Buat virtual environment di folder facepressBE:
            <pre>python -m venv env</pre>
        </li>
        <li>Aktifkan virtual environment:
            <pre>.\env\Scripts\activate</pre>
        </li>
        <li>Masuk ke direktori facepress:
            <pre>cd facepress</pre>
        </li>
        <li>Install semua dependensi:
            <pre>pip install absl-py==2.1.0 asgiref==3.8.1 astunparse==1.6.3 certifi==2024.8.30 charset-normalizer==3.4.0 colorama==0.4.6 Django==5.1.2 django-cors-headers==4.5.0 django-extensions==3.2.3 djangorestframework==3.15.2 djangorestframework-simplejwt==5.3.1 facenet-pytorch==2.6.0 filelock==3.16.1 flatbuffers==24.3.25 fsspec==2024.10.0 gast==0.6.0 google-pasta==0.2.0 grpcio==1.67.0 h5py==3.12.1 idna==3.10 Jinja2==3.1.4 joblib==1.4.2 keras==3.6.0 libclang==18.1.1 lz4==4.3.3 Markdown==3.7 markdown-it-py==3.0.0 MarkupSafe==3.0.2 mdurl==0.1.2 ml-dtypes==0.4.1 mpmath==1.3.0 mtcnn==1.0.0 namex==0.0.8 networkx==3.4.2 numpy==1.26.4 opencv-contrib-python==4.10.0.84 opencv-python==4.10.0.84 opt_einsum==3.4.0 optree==0.13.0 packaging==24.1 pillow==10.2.0 protobuf==4.25.5 Pygments==2.18.0 PyJWT==2.9.0 PyMySQL==1.1.1 requests==2.32.3 rest-framework-simplejwt==0.0.2 rich==13.9.3 setuptools==65.5.0 six==1.16.0 sqlparse==0.5.1 sympy==1.13.3 tensorboard==2.17.1 tensorboard-data-server==0.7.2 tensorflow==2.17.0 tensorflow-intel==2.17.0 tensorflow-io-gcs-filesystem==0.31.0 termcolor==2.5.0 torch==2.2.2 torchvision==0.17.2 tqdm==4.66.5 typing_extensions==4.12.2 tzdata==2024.2 urllib3==2.2.3 Werkzeug==3.0.4 wheel==0.44.0 wrapt==1.16.0</pre>
        </li>
        <li>Jalankan perintah berikut untuk migrasi database:
            <ul>
                <li>Generate file migration:
                    <pre>python manage.py makemigrations</pre>
                </li>
                <li>Jalankan migrasi:
                    <pre>python manage.py migrate</pre>
                </li>
            </ul>
        </li>
        <li>Jalankan seeder untuk data awal:
            <ul>
                <li>Admin: <pre>python manage.py admin_seeder</pre></li>
                <li>Dosen: <pre>python manage.py dosen_seeder</pre></li>
                <li>Mahasiswa: <pre>python manage.py mahasiswa_seeder</pre></li>
                <li>Ruang: <pre>python manage.py ruang_seeder</pre></li>
                <li>Mata Kuliah: <pre>python manage.py mata_kuliah_seeder</pre></li>
                <li>Kelas: <pre>python manage.py kelas_seeder</pre></li>
                <li>Jadwal Kelas: <pre>python manage.py jadwal_kelas_seeder</pre></li>
            </ul>
        </li>
        <li>Jalankan server:
            <pre>python manage.py runserver</pre>
        </li>
    </ol>
</body>
