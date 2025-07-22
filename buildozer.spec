!sed -i 's/^requirements = .*/requirements = python3,kivy/' buildozer.spec
!sed -i 's/^source.include_exts = .*/source.include_exts = py,json/' buildozer.spec
!sed -i 's/# android.permissions = INTERNET/android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE/' buildozer.spec
