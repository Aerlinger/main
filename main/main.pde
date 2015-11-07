import processing.sound.*;

SoundFile file;
Table melodyTable;
Table richMelodyTable;
Table beatTable;
Table chordTable;

int frames = 0;
float fps = 30.0;
float pixelsPerSecond = 320.0;

//String filename = "a-drowning.mp3";
//String filename = "end-of-line.mp3";
//String filename = "the-four-of-us-are-dying.mp3";
//String filename = "clutter.mp3";
//String filename = "the-believers.mp3";
String filename = "cider_time.mp3";

void setup() {
  chordTable = loadTable("data/_" + filename + "/chords.csv", "header");
  melodyTable = loadTable("data/_" + filename + "/melody.csv", "header");
  richMelodyTable = loadTable("data/_" + filename + "/melody_detailed.csv", "header");
  beatTable = loadTable("data/_" + filename + "/beat.csv", "header");
  
  size(1800, 360);
  background(64);
  
  for (TableRow row : melodyTable.rows()) {
    println(row.getString("onset_time") + ": " + row.getString("midi_pitch"));
  }
  
  frameRate(fps); 
  
  file = new SoundFile(this, filename);
  file.play();
}

float secondsElapsed() {
  return frames / fps;
}

void draw() {
  frames++;
   textSize(22);
  
  background(20);
  
  text(frames/fps, 50, 50);
 
  stroke(color(0, 255, 0), 255);
  line(pixelsPerSecond * secondsElapsed(), 0, pixelsPerSecond * secondsElapsed(), height);
  
  for (TableRow row : beatTable.rows()) {
    float beatX = pixelsPerSecond * row.getFloat("time");
    boolean downbeat = row.getString("downbeat").equals("true");
    
    fill(color(0, 255, 0), 255);
    stroke(color(0, 255, 0), 255);
    
    float radius = 3.0;
    if(downbeat)
      radius = 8.0;
      
    ellipse(beatX, height - 50, radius, radius);
  }
  
  for (TableRow row : melodyTable.rows()) {
    float noteX = pixelsPerSecond * row.getFloat("onset_time");
    float noteY = 2 * row.getFloat("midi_pitch");
    float duration = row.getFloat("duration");
    
    fill(color(255, 0, 0), 255);
    stroke(color(255, 0, 0), 255);
    rect(noteX, noteY, duration * pixelsPerSecond, 3);
    //println(noteX + ": " + noteY);
  }
  
  for (TableRow row : richMelodyTable.rows()) {
    float noteX = pixelsPerSecond * row.getFloat("onset_time");
    float noteY = 2 * row.getFloat("midi_pitch") - 15;
    
    fill(color(255, 0, 255), 255);
    stroke(color(255, 0, 0), 255);
    ellipse(noteX, noteY, 3, 3);
    //println(noteX + ": " + noteY);
  }
  
  for (TableRow row : richMelodyTable.rows()) {
    float noteX = pixelsPerSecond * row.getFloat("onset_time");
    float noteY = 2 * row.getFloat("midi_pitch") - 15;
    
    fill(color(255, 0, 255), 255);
    stroke(color(255, 0, 0), 255);
    ellipse(noteX, noteY, 3, 3);
    //println(noteX + ": " + noteY);
  }
  
  for (TableRow row : chordTable.rows()) {
    float chordX = pixelsPerSecond * row.getFloat("time");
    float chordY = height/2 - 15;
    
    fill(color(255, 0, 255), 255);
    stroke(color(255, 0, 0), 255);
    line(chordX, chordY - 20, chordX, chordY + 20);
    
    text(row.getString("chord"), chordX, chordY); 
  }
}