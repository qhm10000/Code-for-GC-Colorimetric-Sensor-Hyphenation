1.	#define STEP_PIN 2    
2.	#define DIR_PIN 3  
3.	  
4.	  
5.	void setup() {  
6.	 
7.	  pinMode(STEP_PIN, OUTPUT);    
8.	  pinMode(DIR_PIN, OUTPUT);    
9.	    
10.	   
11.	  digitalWrite(DIR_PIN, LOW);   
12.	}  
13.	  
14.	void loop() {  
15.	  
16.	   
17.	  const long pulseDuration = 23810;  
18.	  long startTime = micros();     
19.	    
20.	  for (int i = 0; i < 21; i++) {    
21.	    digitalWrite(STEP_PIN, HIGH);   
22.	    delayMicroseconds(pulseDuration / 2);    
23.	    digitalWrite(STEP_PIN, LOW);     
24.	    delayMicroseconds(pulseDuration / 2);    
25.	  }    
26.	    
27.	      
28.	  long endTime = micros();    
29.	  long elapsedTime = endTime - startTime;    
30.	  long remainingTime = 1000000 - elapsedTime;   
31.	  if (remainingTime > 0) {    
32.	    delayMicroseconds(remainingTime);    
33.	  }    
34.	}  
