#±àÒëfftÄ£¿éµÄ¾²Ì¬¿â£¬make clean & make

SRC = ./native/src/geophone.c ./native/src/analyze.c
TARGET = FFT.so
INCLUDE_PATH = ./native/include
PYTHON_PATH = ./python
FLAG = -shared -fpic -lpython -I $(INCLUDE_PATH)
COMPILOR = gcc

MSG_BEGIN = -------- begin --------
MSG_END = --------  end  --------
MSG_ERRORS_NONE = Error: NONE
MSG_CLEANING = Cleaning project:
REMOVE = rm -f

all:
	@echo $(MSG_BEGIN) 
	$(COMPILOR) $(FLAG) $(SRC) -o $(TARGET)
	@echo "generated", $(TARGET)
	@echo $(MSG_ERRORS_NONE)
	@echo $(MSG_END)
	cp $(TARGET) $(PYTHON_PATH)
	
begin:
	@echo $(MSG_BEGIN)

finished:
	@echo $(MSG_ERRORS_NONE)
	
end:
	@echo $(MSG_END)
	
clean_list :
	@echo $(MSG_CLEANING)
	$(REMOVE) $(TARGET).so	
clean:  clean_list  	