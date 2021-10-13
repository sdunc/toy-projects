typedef union SomeValue {
  int anInt;
  float afloat;
  char* name;
} SomeValue;


int main()
{
  SomeValue x;
  x.anInt = 42;
  return 0;
}
  
