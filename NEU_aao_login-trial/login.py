# -*- coding: GBK -*-
import urllib2
import urllib
import cookielib
import tesseract 
import re

def getCookieJar(url):
    """
    Return a cookieJar of an url.
    @param url: the url of login page
    @return: a cookieJar
    """
    cookieJar = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    opener.open(url)
    return cookieJar

def getImage(imageUrl, cookieJar):
    """
    Use a cookieJar to get the binary image data of imageUrl.
    @param imageUrl: the url of the image.
    @param cookieJar: the cookieJar
    @return: the binary data of image
    """
    img_request = urllib2.Request(imageUrl)
    img_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    return img_opener.open(img_request).read()

def tesseractTrans(img_binary_data): 
    """
    Translate image to text using python-tesseract.
    WARNING: To better translate, the code below has specified some paragrams:
        e.g.    api.Init(".", "eng", tesseract.ORIENTATION_PAGE_RIGHT)
                api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz")
                api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)
        Please adjust the paragram befor you try to run this program.
    @param img_binary_data: the binary data of img.
    @return: the translated text
    """
    api = tesseract.TessBaseAPI()
    api.Init(".", "eng", tesseract.ORIENTATION_PAGE_RIGHT)
    api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz")
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)
    code = tesseract.ProcessPagesBuffer(img_binary_data, len(img_binary_data), api)
    # It's probably a bug in tesseract: the end of the output file is appended two extra blank lines.
    code = code.split()[0]
    return code


def login(url, username, password, code, cookieJar):
    """
    Use specified username, password, code, cookieJar to login the url.
    @param url: the login url
    @param username: your user name
    @param password: your user password
    @param code: the verification code of the website
    @param cookieJar: contains the cookie of this simulated login
    """
    # generate postdata
    data = {
            "WebUserNO" : username,
            "Password" : password,
            "Agnomen" : code
    }
    postdata = urllib.urlencode(data)
    request = urllib2.Request(url, postdata)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    return opener.open(request).read()

def requestScore(scoreUrl, cookieJar):
    """
    Use the scoreUrl to get the html content of score.
    @param scoreUrl: score url
    @param cookieJar: the cookie that have been tagged login
    @return the html content of score page
    """
    request = urllib2.Request(scoreUrl)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    return opener.open(request).read()


def getText(data):
    list = []
    temp = ''
    for x in data.split('\n'):
        if x.find(r'<!--<td align="center" nowrap></td>') != -1:
            continue
        else:
            if x.find(r'<td height="28" align="center" nowrap>') != -1:
                temp = x[42:x.find(r'<\td>')-5]
#                 print temp, '\n-----------------------------'
                list.append(temp)
            if x.find(r'<td align="center" nowrap>') != -1:
                if x.find(r'--><td align="center" nowrap>') != -1:
                    temp = x[33:x.find(r'<\td>')-5]
#                     print temp, '\n-----------------------------'
                    list.append(temp)
                else:
                    temp = x[30:x.find(r'<\td>')-5]
#                     print temp, '\n-----------------------------'
                    list.append(temp)
            if x.find(r'<td nowrap>&nbsp;') != -1:
                temp = x[21:x.find(r'<\td>')-5]
#                 print temp, '\n-----------------------------'
                list.append(temp)
    return list
        
                

if __name__ == "__main__":
    
    url = 'http://202.118.31.197/ACTIONLOGON.APPPROCESS?mode='
    username = '20135072'
    password = '97033925'
    imageUrl = 'http://202.118.31.197/ACTIONVALIDATERANDOMPICTURE.APPPROCESS'
    scoreUrl = 'http://202.118.31.197/ACTIONQUERYSTUDENTSCORE.APPPROCESS'
    
    cookieJar = getCookieJar(url)
    image = getImage(imageUrl, cookieJar)
    code = tesseractTrans(image)
    print 'identifyingCode:', code
    login_html = login(url, username, password, code, cookieJar)
#     print login_html
    score_html = requestScore(scoreUrl, cookieJar)
#     print score_html
    list = getText(score_html)
    for x in list:
        print x
 
    
    
    
    
    
    
