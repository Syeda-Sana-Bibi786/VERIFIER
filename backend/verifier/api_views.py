from django.shortcuts import render
#packages for links
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#packages common for links and images
from rest_framework.decorators import api_view
from rest_framework.response import Response
#packages for image
#from PIL import Image
#from PIL.ExifTags import TAGS

#threat detection list
SUSPICIOUS_TLDS=['.xyz','.tk','.zip','.ru','.click','.ml','.cf']
SUSPICIOUS_KEYWORDS=['upi','kyc','aadhar','aadhaar','pan','loan','payment','verfy','cashback','reward','support','account','phonepe','paytm','sbi','hdfc','icici']
SHORTENERS=['bit.ly','tinyurl.com','t.co','goo.gl']
#to get site preview
def get_site_preview(url):
    try:
        headers={"User-Agent":"Mozilla/5.0"}
        response=requests.get(url,timeout=5)
        soup=BeautifulSoup(response.content,'html.parser')
        title_tag=soup.find('title')
        title=title_tag.get_text(strip=True) if title_tag else "No title found!"
        meta=( soup.find("meta",attrs={"name":"description"})
              or soup.find("meta",attrs={"name":"Description"})
              or soup.find("meta",attrs={"property":"og:description"})
        )
        description=meta["content"].strip() if meta and "content" in meta.attrs else "No description found!"
        return{
            "title":title ,
            "description":description
        }
    except:
        return{
            "title":"N/A" , "description":"Couldn't find preview"
        }  
#veryfying link
@api_view(['POST'])
def verify_link(request):
    url=request.data.get('url')
    if not url:
        return Response({"error":"Url is not given"},status=400)
    try:
        response=requests.get(url,timeout=6,allow_redirects=True)
        final_url=response.url
        #parsing the url
        parsed=urlparse(final_url)
        domain=parsed.netloc.lower()
        path=parsed.path.lower()
        tld='.'+domain.split('.')[-1]
        #checking for red flags
        is_ip=re.match(r'^\d{1,3}(\.\d{1,3}){3}$',domain)
        is_bad_tld=tld in SUSPICIOUS_TLDS
        is_bad_keyword=any(kw in path or kw in domain for kw in SUSPICIOUS_KEYWORDS)
        is_shortened=any(short in url for short in SHORTENERS)
        #checking suspicious or not
        is_suspicious=bool(is_ip or is_bad_tld or is_bad_keyword or is_shortened)
        site_preview=get_site_preview(final_url)
        print(f"[DEBUG] Final URL:{final_url}")
        print(f"[DEBUG] Suspicious:{is_suspicious}")
        print(f"[DEBUG] Preview:{site_preview}")
        return Response(
            {
                "data":{
                    "original_url":url,
                    "final_url":final_url,
                    "safety_verdict":"✅Link appears safe , you can go ahead." if not is_suspicious else "⚠️Suspicious link, be careful",
                    "site_preview":site_preview
                }
            }
        )
    except Exception as e:
        return Response({"error":f"Error checking link : {str(e)}"},status=500)
'''
# image code
@api_view(['POST'])
def verify_image(request):
    image_file=request.FILES.get('image')
    if not image_file:
        return Response({"error":"No image uploaded"},status=400)
    try:
        image=Image.open(image_file)
        exif_data=image._getexif() 
        
        
        if not exif_data:
            return Response({
                "Result" : "❌No EXIF metadata is found!",
                "Verdict" : "⚠️ Possibly a screenshot or AI generated  or downloaded from internet"
            })
        readable={TAGS.get(tag): str(value) for tag,value in exif_data.items() for tag in TAGS}
        software=readable.get("Software","").lower()
        make=readable.get("Make","")
        model=readable.get("Model","")
        datetime=readable.get("DateTime","")
        if "photoshop" in software or "editor"  in software or "canva" in software:
            verdict="⚠️ Metadata shows image was likely edited "
        elif make or model:
            verdict="✅Image appears original (camera details found)"
        else:
            verdict="⚠️Metadata found but origin is unclear"
        return Response({
            "result":"✅EXIF metdata found",
            "device_make":make,
            "device_model":model,
            "taken_on":datetime,
            "software_used":software if software else "Not specified",
            "verdict":verdict
        })
    except Exception as e:
        return Response({"error":f"Error reading image : {str(e)}"},status=500)
        '''