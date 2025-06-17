from django.db import migrations


def create_default_rank(apps, schema_editor):
    rank = apps.get_model('ranks', 'Rank')
    rank.objects.create(
        name='E-1',
        description='<ol><li>Interest in becoming a member of Black Widow Company</li><li>Post a complete recruitment application in the recruitment area of the forums</li><li>Registered on OpServ</li><li>Activated TeamSpeak</li></ol>',
        icon='ranks/icon/[FORUM]-Recruit.png',
        fs_icon='ranks/fs/[FS]-Recruit.png',
        color_hex='#FFFF00',
        is_active=True,
        is_default=True,
        order=0
    )


class Migration(migrations.Migration):
    dependencies = [
        ('ranks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_rank, reverse_code=migrations.RunPython.noop),
    ]
