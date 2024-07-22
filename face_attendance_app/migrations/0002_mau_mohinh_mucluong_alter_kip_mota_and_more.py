# Generated by Django 4.1.13 on 2024-07-22 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('face_attendance_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=255)),
                ('ngayThem', models.DateTimeField()),
                ('nhanVien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_attendance_app.nhanvien')),
            ],
        ),
        migrations.CreateModel(
            name='MoHinh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('ngayTrain', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MucLuong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('luong', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='kip',
            name='moTa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lichlamviec',
            name='moTa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ngay',
            name='moTa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='MucLuongNhanVien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngayCoHieuLuc', models.DateField()),
                ('mucLuong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_attendance_app.mucluong')),
                ('nhanVien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_attendance_app.nhanvien')),
            ],
        ),
        migrations.CreateModel(
            name='MauMoHinh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_attendance_app.mau')),
                ('moHinh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_attendance_app.mohinh')),
            ],
        ),
    ]
