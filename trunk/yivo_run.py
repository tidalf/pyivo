from logic.application import YivoApplication
import sys



if __name__ == '__main__':
    try: 
        yivo = YivoApplication(None)
        yivo.run()
    except:
        type,value,trace = sys.exc_info()
        print 'Error:', value
    
    
	