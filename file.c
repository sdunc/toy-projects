int main()
{
  /* low level directly call os  */
  int myFile = open(...);

  /* buffered io, far better for large files */
  FILE* myFile = fopen(...);
    
  int trulyTheFile = fileno(myFile);
}
