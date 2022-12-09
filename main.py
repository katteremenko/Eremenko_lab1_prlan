import requests
import sys
import time
  
units = {    
'B'  : {'size':1},
'KB' : {'size':1024},
'MB' : {'size':1024*1024},
'GB' : {'size':1024*1024*1024}
}
  
def check_unit(length): 
    if length < units['KB']['size']:
        return 'B'
    elif length >= units['KB']['size'] and length <= units['MB']['size']:
        return 'KB'
    elif length >= units['MB']['size'] and length <= units['GB']['size']:
        return 'MB'
    elif length > units['GB']['size']:
        return 'GB'
  
def downloadFile(url, directory) :
  
    localFilename = url.split('/')[-1]
  
    with open(directory + '/' + localFilename, 'wb') as f:
        r = requests.get(url, stream=True)
        total_length = float(r.headers.get('content-length')) 
        d = 0 
        if total_length is None:
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):                 
                d += float(len(chunk))
                f.write(chunk)

                downloaded = d/units[check_unit(d)]['size']
                tl = total_length / units[check_unit(total_length)]['size']
  
                sys.stdout.write("\r %7.2f%s  /  %4.2f %s" % (downloaded, check_unit(d), tl, check_unit(total_length)))
                sys.stdout.flush()
  
def main() :
    directory = '.'
    if len(sys.argv) > 1 :
        url = sys.argv[1]          
        downloadFile(url, directory)
        print ("\nFile downloaded!")
    else :
        print("Link doesn't exist!")
  
if __name__ == "__main__" :
    main()