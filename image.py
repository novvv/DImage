#~""" doc - примитивный документ """
from OFS import SimpleItem,ObjectManager,PropertyManager,Folder,Image
from PIL import Image as AImage,ImageDraw

from Shared.DC.ZRDB.Results import Results
from  Shared.DC.ZRDB.RDB import File
from cStringIO import StringIO
import StringIO

from Globals import DTMLFile
from DateTime import DateTime
import Products
from types import *
import sys
#from ZODB.PersistentList import PersistentList
from AccessControl import ClassSecurityInfo
from threading import Lock   
#==============================================

l = Lock()

class DImage(Image.Image):
    """
    An Image product
    """
    meta_type = 'DImage'

    manage_options =  (
    #{'label': 'Просмотр', 'action': 'index_html',},
    {'label': 'Изменить', 'action': 'manage_editForm',},    
    )    + Image.Image.manage_options

#    index_html = DTMLFile('www/index_html',        globals()) # Used to view content of the object
    manage_editForm = DTMLFile('www/manage_editForm',globals()) # Used to view content of the object
        
    def __init__(self, id, title, width, height):
        "Inits the product with default values"
        image=AImage.new('RGB',(width,height))
        #self.width=width
        #self.height=height
        self.script=''
        file=StringIO.StringIO()
        image.save(file,'gif')        
        Image.Image.__init__(self,id=id,title=title,file=file)
    
    def getType(self):
        if hasattr(self,'content_type'):
	   return str(self.content_type.split('/')[1])
	else:
	   return 'gif'
   
    def draw(self,args={},REQUEST=None):
        "draw content"
	
	if hasattr(self,'background'):	    
	    fp=StringIO.StringIO()
	    fp.write( str(self.data) )
	    fp.seek(0) 
	    image=AImage.open(fp)
	    image.load()
	    #image.fromstring(str(self.data))
	else:
	    image=AImage.new('RGB',(int(self.width),int(self.height)))

        canvas=ImageDraw.Draw(image)
        globals=ImageDraw.__dict__
        globals['canvas']=canvas
        globals['self']=self
        globals['image']=image
        if REQUEST:
            pass
        exec(self.script,globals,args)
        file=StringIO.StringIO()
        image.save(file,self.getType()) 
	file.seek(0) 
	return file 
        #self.manage_upload(file)
    
    def index_html(self, REQUEST, RESPONSE):
        "Show dynamic image"
	l.acquire()
        try:
            file=self.draw(); 
    	    REQUEST.RESPONSE.setHeader("Content-Type", "image/"+self.getType()) 
    	    REQUEST.RESPONSE.write(file.read()) 
	    l.release()
    	    return;
        except:
            exc, err = sys.exc_info()[:2]
	    l.release()
            return '<table width='+str(self.width)+'px height='+str(self.height)+'><tr><td>Image rendering error:%s   -  %s</table>' %  (exc, err)
        

        
    
    def scriptEdit(self,REQUEST):
        "edit script"
        self.script=REQUEST.form['script']

def manage_addImageAction(self, id='slot',title='',width=32,height=32,REQUEST=None):
    "Add a hist Slot to a folder."
    self._setObject(id, DImage(id,title,width,height))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

manage_addImageForm=DTMLFile('www/manage_addForm',
        globals())    
