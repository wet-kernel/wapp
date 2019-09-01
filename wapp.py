
import os, shutil, py_compile, sys

sys.path.extend(["/lib"])

def startupdirs():
    if not os.path.isdir ("/var/cache/wapp"): os.mkdir ("/var/cache/wapp")
    if not os.path.isdir ("/var/cache/wapp/archives"): os.mkdir ("/var/cache/wapp/archives")
    if not os.path.isdir ("/var/cache/wapp/archives/build"): os.mkdir ("/var/cache/wapp/archives/build")
    if not os.path.isdir ("/var/cache/wapp/archives/code"): os.mkdir ("/var/cache/wapp/archives/code")
    if not os.path.isdir ("/var/cache/wapp/archives/data"): os.mkdir ("/var/cache/wapp/archives/data")
    if not os.path.isdir ("/etc/wapp"): os.mkdir ("/etc/wapp")

startupdirs()

import libwet

if sys.argv[1]=="--create" or sys.argv[1]=="-c":
    if os.path.isfile ("/var/cache/wapp/archives/lock"):
        libwet.colors.show ("wapp","error","package manager is lock.")
    if os.path.isfile (sys.argv[3]):
        lock = open ("/var/cache/wapp/archives/lock","w")
        lock.close()
        py_compile.compile(sys.argv[3],"/var/cache/wapp/archives/build/control.pyc")
        sys.path.extend(['/var/cache/wapp/archives/build'])
        import control
        if control.data == True:
            libwet.archive.create_data(control.find_data)
        if control.code == True:
            libwet.archive.create_code(control.find_code)
        shutil.make_archive(sys.argv[2],"zip","/var/cache/wapp/archives/build")
        os.rename(sys.argv[2]+".zip",sys.argv[2]+".wet")
        shutil.rmtree("/var/cache/wapp/archives")
    else:
        libwet.colors.show ("wapp","error",str(sys.argv[3]) +": control file not found.")

elif sys.argv[1]=="--install" or sys.argv[1]=="-i":
    if os.path.isfile ("/var/cache/wapp/archives/lock"):
        libwet.colors.show ("wapp","error","package manager is lock.")
    if os.path.isfile (sys.argv[2]+".wet"):
        shutil.unpack_archive(sys.argv[2]+".wet","/var/cache/wapp/archives/build","zip")
        sys.path.extend(['/var/cache/wapp/archives/build'])
        import control
        if control.code == True:
            libwet.archive.unpack_code()
        if control.data == True:
            libwet.archive.unpack_data("@unpack")
        else:
            os.mkdir ("/tmp/data")
            libwet.archive.create_data("/tmp/data")
            os.rmdir("/tmp/data")
        if control.code == True:
            if control.compiler == True:
                for file in control.compile:
                    srcdest = str(file).split(":")
                    libwet.archive.compile(srcdest[0], srcdest[1])
        libwet.archive.wrapp_data()
        libwet.archive.unpack_data(control.unpack)
        for list in control.applist:
            os.system ("chmod +x "+list)
        controls = "/etc/wapp/"+str(control.name)
        if not os.path.isdir (controls):
            os.mkdir(controls)
        shutil.copy("/var/cache/wapp/archives/build/control.pyc",controls+"/control.pyc")
        shutil.rmtree("/var/cache/wapp/archives")
    else:
        libwet.colors.show ("wapp","error",str(sys.argv[2]) +": package file not found.")

elif sys.argv[1]=="--remove" or sys.argv[1]=="-r":
    controls = "/etc/wapp/" + sys.argv[2]
    if os.path.isfile (controls+"/control.pyc"):
        sys.path.extend([controls])
        import control
        for i in control.applist:
            if os.path.isfile(i):
                os.remove(i)
            elif os.path.isdir(i):
                os.rmdir(i)
        shutil.rmtree(controls)
    else:
        libwet.colors.show ("wapp","error",str(sys.argv[2]) +": package not found.")
elif sys.argv[1]=="--compile":
    if os.path.isfile ("/var/cache/wapp/archives/lock"):
        libwet.colors.show ("wapp","error","package manager is lock.")
    if os.path.isfile (sys.argv[3]+".wet"):
        lock = open ("/var/cache/wapp/archives/lock","w")
        lock.close()
        shutil.unpack_archive(sys.argv[3]+".wet","/var/cache/wapp/archives/build","zip")
        sys.path.extend(['/var/cache/wapp/archives/build'])
        import control
        if control.code == True:
            libwet.archive.unpack_code()
        if control.data == True:
            libwet.archive.unpack_data("@unpack")
        else:
            os.mkdir("/tmp/data")
            libwet.archive.create_data("/tmp/data")
            os.rmdir("/tmp/data")
        if control.code == True:
            if control.compiler==True:
                for file in control.compile:
                    srcdest = str(file).split(":")
                    libwet.archive.compile(srcdest[0], srcdest[1])
        libwet.archive.wrapp_data()
        os.remove("/var/cache/wapp/archives/build/code.tar.xz")
        file = open("/tmp/control","w")
        file.write("name = \""+control.name+"\"\n")
        file.write("release = \""+control.release+"\"\n")
        file.write("version = \""+control.version+"\"\n")
        file.write("copyright = \""+control.copyright+"\"\n")
        file.write("license = \""+control.license+"\"\n")
        file.write("code = False\n")
        file.write("data = True\n")
        file.write("unpack = \""+control.unpack+"\"\n")
        strv = ""
        for list in control.applist:
            if strv == "":
                strv = strv + "\"" + list +"\""
            else:
                strv = strv + ", \"" + list +"\""
        file.write("applist = [ " + strv + "]\n")
        file.close()
        py_compile.compile("/tmp/control","/var/cache/wapp/archives/build/control.pyc")
        shutil.make_archive(sys.argv[2],"zip","/var/cache/wapp/archives/build")
        os.rename(sys.argv[2]+".zip",sys.argv[2]+".wet")
        shutil.rmtree("/var/cache/wapp/archives")
    else:
        libwet.colors.show ("wapp","error",str(sys.argv[3]) +": package file not found.")

elif sys.argv[1]=="--clean":
    shutil.rmtree("/var/cache/wapp/archives")
elif sys.argv[1]=="--info":
    if os.path.isfile ("/etc/wapp/"+str(sys.argv[2])+"/control.pyc"):
        controls = "/etc/wapp/" + str(sys.argv[2])
        sys.path.extend([controls])
        import control

        name = control.name
        release = control.release
        copyright = control.copyright
        license = control.license
        version = control.version

        print(
            "    Package name: " + name + "\n" +
            " Package version: " + version + "\n" +
            " Package release: " + release + "\n" +
            "       Copyright: " + copyright + "\n" +
            "         License: " + license
        )
    else:
        libwet.colors.show ("wapp","error",str(sys.argv[2]) +": package not found.")
else:
    libwet.colors.show("wapp", "error", str(sys.argv[1]) + ": wrong option.")
