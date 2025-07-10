from django.shortcuts import render
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response
#image verification
from PIL import Image
from PIL.ExifTags import TAGS



SAFE_BROWSING_URL=f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
#google safe browsing
def check_google_safe_browsing(final_url):
    payload={
            "client":{
                "clientId":"verifyAI",
                "clientVersion":"0.01"
            },
            "threatInfo":{
                "threatTypes":["MALWARE","SOCIAL_ENGINEERING","UNWANTED_SOFTWARE","POTENTIALLY_HARMFUL_APPLICATION"],
                "platfromTypes":["ANY_PLATFORM"],
                "threatEntryTypes":["URL"],
                "threatEntries":[{"url":final_url}]
            }
        }
    try:
        sb_response=requests.post(SAFE_BROWSING_URL,json=payload)
        sb_result=sb_response.json()
        if sb_result.get("matches"):
            return "⚠️Unsafe Link detected by Google Safe Browsing."
        else:
            return "✅Link appears safe"
    except Exception:
        return "❓Unable to verify with Google Safe Browsing"
#site preview
def get_site_preview(response_text):
    try:
        soup=BeautifulSoup(response_text,'html.parser')
        title_tag=soup.title
        title=title_tag.string.strip() if (title_tag and title_tag.string ) else "No title found"
        desc_tag=soup.find("meta",attrs={"name":"description"}) or soup.find("meta",attrs={"name":"Description"}) or soup.find("meta",attrs={"property":"og:description"})
        description=desc_tag['content'].strip() if desc_tag and 'content' in desc_tag.attrs else "No description found"
        return title,description
    except Exception:
            title,description="Error reading page","No description"
#api view (used by frontend & discord bot)
@api_view(['POST'])
def verify_link(request):
    url=request.data.get('url')
    print("Recieved URL:",url)
    if not url:
        return Response({"error":"No URL provided"},status=400)
    #normal url
    parsed_url=urlparse(url)
    if not parsed_url.scheme:
        url="http://"+url
    try:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64;x64)'
        }
        response=requests.get(url,headers=headers,timeout=5,allow_redirects=True)
        final_url=response.url
        #calling google safe browsing function
        verdict=check_google_safe_browsing(final_url)
        #verdict="✅skipping google check"
        #call site preview functio
        title,description=get_site_preview(response.text)
        #title,description="title","desc"
        return Response({
            "Original_URL":url,
            "Final_URL":final_url,
            "Safety_Verdict":verdict,
            "Title":title,
            "Description":description
        })
    except Exception as e:
        return Response({"error":f"Error fetching URL : {str(e)}"},status=500)
#frontend views
def home(request):
    return render(request,'home.html')
def verify_link_frontend(request):
    result=None
    if request.method=='POST':
        url=request.POST.get('url')
        try:
            response=requests.post('http://127.0.0.1:8000/api/verify-link/',json={"url":url})
            if response.status_code==200:
                result=response.json()  
            else:
                result={"error":"Failed to verify link."}
        except Exception as e:
            result={"error":f"Error:{str(e)}"}
    return render(request,'verify_link.html',{'result':result})
#image verification api view
@api_view(['POST'])
def verify_image(request):
    image_file=request.FILES.get('image')
    if not image_file:
        return Response({"error":"No image uploaded"},status=400)
    try:
        image=Image.open(image_file)
        print("image format : ",image.format)
        #trying to extract exif 
        exif_data=image._getexif()
        width,height=image.size
        file_format=image.format
        print("exif data recieved",exif_data)
        if exif_data:
            useful_tags=['Software','DateTimeOriginal','Make','Model','DateTime']
            readable_exif={TAGS.get(tag):str(value) for tag,value in exif_data.items() if TAGS.get(tag) in useful_tags}
            return Response({
                "result":"✅EXIF metadata found!",
                "format":file_format,
                "exif":readable_exif
            })
        #if no exifs then lets analyze dimensions
        #width,height=image.size
        #file_format=image.format#jpeg or png
        if width<1500 and height<1500:
            verdict="⚠️No EXIF found. Resoultion suggests screenshot or mobile capture."
        elif width>=3000 or height>=3000:
            verdict="⚠️No EXIF found. High Resoultion suggests AI-generated or DSLR."
        elif 1500<=width<3000 or 1500<=height<3000:
            verdict="⚠️No EXIF found. Medium Resoultion suggests downloaded or edited image."
        else:
            verdict="⚠️No EXIF found.COuld not confidently classify."
        #file format hint
        if file_format=='PNG':
            verdict+=" (PNG format-higher chance it is screenshot)"
        return Response({
            "result":verdict,
            "width":width,
            "height":height,
            "format":file_format
        }
        )
    except Exception as e:
        return Response({"error":f"Error reading image:{str(e)}"},status=500)
#image verification frontend
def verify_image_frontend(request):
    result=None
    if request.method=='POST':
        image_file=request.FILES.get('image')
        try:
            response=requests.post('http://127.0.0.1:8000/api/verify-image/',files={'image':image_file})
            if response.status_code==200:
                result=response.json()
            else:
                result={"error":"Failed to verify image."}
        except Exception as e:
            result={"error":f"Error:{str(e)}"}
    return render(request,'verify_image.html',{'result':result})
    