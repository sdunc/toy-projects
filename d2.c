#include <stdio.h>
#include <stdlib.h>


/* size_t getDelim(char** lineptr, size_t* linecap, int delimiter, FILE* fptr) { */
/*   /\* reads a line from stream delimited by the character */
/*      delimiter. may provide a pointer to a malloced buffer for the */
/*      line in lineptr and the capacity of that buffer in linecap. the */
/*      buffer is expanded if needed via realloc(). in either case *linep */
/*      and *linecapp will be updated accordingling *\/ */
/*   // time difference of this vs other implementations */
/*   int linelen = 0; */
/*   printf("got a pointer to line at %d, with a length %d\n",*lineptr,*linecap); */
/*   return n; */
/* } */
  
  /* while ( !feof(fptr) ) { this is bad because we will read an extra
     time. eof is only asserted after we have read past the end of our
     buffer. instead treat the call to read more from the buffer as
     the faulty operation taht it is. */
  /* int linelen = 8; */
  /* char* direction = malloc(sizeof(char)*linelen); */

  /* for (;;) { */
  /*   size_t n = getDelim(&direction, &line_len, ' ', FILE* fptr); */
  /*   if (n == 0) { break; } */
    
    
  /*   } */




size_t getDelim(FILE* fp, char** lineptr, char delim) {
  /* Read from FILE* fp a string up to and excluding a char delim,
  place into string_buffer, return number of characters read into
  string_buffer */
  char c;
  int bytesRead = 0;
  int arraySize = 8;
  *lineptr = calloc(arraySize, sizeof(char)*arraySize);
  
  while ( !feof(fp) ) {
    c = fgetc(fp);
    if ( c == delim ) return bytesRead;
    else if (bytesRead == arraySize) {
      arraySize *= 2;
      *lineptr = realloc(lineptr, arraySize);
      for (int i=bytesRead; i<arraySize; i++)
	(*lineptr)[i] = 0;	
    }
    (*lineptr)[bytesRead] = c;
    bytesRead++;
  }
  // we reached the eof before the delim
  // free the lineptr and return 0 bytes read
  free(*lineptr);
  return 0;
}

int strCmp(char* s1, char* s2) {
  while (*s1 != 0 || *s2 != 0) {
    if (*s1 != *s2) return 1;
    s1++;
    s2++;
  }
  if (*s1 == *s2) return 0;
  else return 1;
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
  if (argc < 2) { printf("Usage: ./d2 [input file]\n"); return -1; }

  int getting_direction = 1; // bool, 1 if we need to get directioon sill
  int x; // forward
  int depth; // up, down
  char* strBuffer; // max 32bit int is 9chars long
  char* numBuffer;
  int sbi = 0;
  int dist = 0;
  int aim = 0;

  FILE* fp;
  
  fp = fopen(argv[1], "r");
  if (fp < 0) { printf("error! could not open [%s].\n",argv[1]); return -1; }

  while ( getDelim(fp, &strBuffer, ' ') > 0 ) {
    getDelim(fp, &numBuffer, '\n');
    dist = atoi(numBuffer);
    printf("read string %s and distance %d\n", strBuffer, dist);
    if ( strCmp(strBuffer,"forward")==0) {
      x += dist;
      depth += (aim*dist);
      /* printf("going forward!\n");       */
    }
    else if ( strCmp(strBuffer,"up")==0) {
      /* depth -= dist; */
      aim -= dist;
      /* printf("going up!\n"); */
    }
    else if (strCmp(strBuffer,"down")==0) {
      /* printf("going down!\n"); */
      aim += dist;
      /* depth += dist; */
    }
    free(strBuffer);
    free(numBuffer);
  }

  fclose(fp);
  printf("ended up at coords x=%d, y=%d, x*y=%d\n",x,depth,x*depth);
  
  return 0;
}














