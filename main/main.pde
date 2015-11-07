import processing.sound.*;

SoundFile file;
Table melodyTable;
Table beatTable;

int frames = 0;
float fps = 30.0;
float pixelsPerSecond = 30.0;

void setup() {
  melodyTable = loadTable("data/clutter/melody.csv", "header");
  beatTable = loadTable("data/clutter/beat.csv", "header");
  
  size(1600, 360);
  background(64);
  
  for (TableRow row : melodyTable.rows()) {
    println(row.getString("onset_time") + ": " + row.getString("midi_pitch"));
  }
  
  frameRate(fps); 
  
  file = new SoundFile(this, "clutter/audio.mp3");
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
    
    fill(color(0, 255, 0), 255);
    stroke(color(0, 255, 0), 255);
    ellipse(beatX, height - 50, 3, 3);
  }
  
  for (TableRow row : melodyTable.rows()) {
    float noteX = pixelsPerSecond * row.getFloat("onset_time");
    float noteY = 2 * row.getFloat("midi_pitch");
    
    fill(color(255, 0, 0), 255);
    stroke(color(255, 0, 0), 255);
    ellipse(noteX, noteY, 3, 3);
    println(noteX + ": " + noteY);
    //println(row.getString("onset_time") + ": " + row.getString("midi_pitch"));
  }
}