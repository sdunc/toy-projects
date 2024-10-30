#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>

size_t getDelim(FILE* fp, char** lineptr, char delim) {
  /* Read from FILE* fp a string up to and excluding a char delim,
  place into string_buffer, return number of characters read into
  string_buffer */
  char c;
  int bytesRead = 0;
  int arraySize = 8;
  *lineptr = malloc(sizeof(char)*arraySize);
  
  while ( !feof(fp) ) {
    c = fgetc(fp);
    if ( c == delim ) return bytesRead;
    else if (bytesRead == arraySize) {
      arraySize *= 2;
      *lineptr = realloc(*lineptr, arraySize);
    }
    (*lineptr)[bytesRead] = c;
    bytesRead++;
  }
  // we reached the eof before the delim
  // free the lineptr and return 0 bytes read
  free(*lineptr);
  return 0;
}

int stoi(char* sb, int len_sb) {
  int value = 0;
  int placeWeight = 1;
  for(int i=len_sb-1; i>=0; i--) {
    value+= (sb[i]*placeWeight);
    placeWeight*=10;
  }
  return value;
}


int main(int argc, char* argv[]) {
  if (argc < 2) { printf("Usage: ./d1 [input file]\n"); return -1; }

  int part = 2;
  int stageInWindow = 0; // 0 1 2 = % 3, at 2 we have new measurement
  // a sliding window is kinda like a pipeline, the first three
  // measurements fill the pipeline and then each following one will
  // have a new 3 window avg
  int timesHigher;
  int lastLine;
  int thisLine;
  int bytesRead;   // check return values of library functions.
  char* strBuffer; // max 32bit int is 9chars long
  int sbi = 0;
  int fd;
  int windowSum = 0;
  int window0;
  int window1;
  int window2;

  /* /\* fd = open(argv[1], O_RDONLY); *\/ */

  FILE* fp;
  
  fp = fopen(argv[1], "r");
  if (fp < 0) { printf("error! could not open [%s].\n",argv[1]); return -1; }

  bytesRead = getDelim(fp, &strBuffer, '\n');
  lastLine =  atoi(strBuffer);
  if (part == 2) {
    // set up the window
    window0 = lastLine; 
    windowSum+=window0;
    getDelim(fp, &strBuffer, '\n');
    window1 =  atoi(strBuffer);
    windowSum+=window1;
    getDelim(fp, &strBuffer, '\n');
    window2 =  atoi(strBuffer);
    windowSum += window2;
  }

  while ( fscanf(fp, "%d", &thisLine) > 0 ) {
    if (part == 1) {
      printf("%d\n",thisLine);
      if (thisLine > lastLine) timesHigher++;
      lastLine = thisLine;
    }
    else {
      printf("%d\n",thisLine);
      // A new int has been read into thisLine
      // compare to old window value and increment counter if
      // our window has increased
      if (windowSum-window0+thisLine > windowSum)
	timesHigher++;
      windowSum-=window0; // remove old value
      windowSum+=thisLine; // add new val to window
      // shift over tracking variables
      window0 = window1;
      window1 = window2;
      window2 = thisLine;
    }
  }

  fclose(fp);
  printf("Increased %d times in input file %s\n",timesHigher, argv[1]);
  return 0;
}














