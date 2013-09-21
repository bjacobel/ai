package Vision;

// **********************
// *                    *
// *  Simulated Camera  *
// *                    *
// **********************

import java.util.Random;
import java.util.Vector;

public class Camera
{
  // ****************
  // *              *
  // *  Statistics  *
  // *              *
  // ****************
  public class Stats
  {
    double sum, sum2;
    int n;
    double lo, hi;
    
    // effect   Clear all statistics
    public void clear()
    {
      n = 0;
      lo = hi = 0;
    }
    
    // effect   Add the specified value to the statistics
    public void add(double x)
    {
      if (n == 0)
      {
        sum = x;
        sum2 = x * x;
        lo = hi = x;
      }
      else
      {
        sum += x;
        sum2 += x * x;
        lo = Math.min(lo, x);
        hi = Math.max(hi, x);
      }
      ++n;
    }
    
    // returns  The number of samples
    public int count() { return n;}
    
    // returns  The mean value, or 0 if no samples yet given
    public double mean() { return n > 0 ? sum / n : 0.0;}
    
    // returns  The standard deviation, or 0 if less than two samples given
    public double stDev()
    {
      return n > 1 ? Math.sqrt(n * sum2 - sum * sum) / n : 0.0;
    }
    
    // returns  The minimum value, or 0 if no samples yet given
    public double min() { return lo;}
    
    // returns  The maximum value, or 0 if no samples yet given
    public double max() { return hi;}
    
    // effect   Print the current statistics on the system console, using
    //          one line.
    public void print(String name)
    {
      System.out.printf("%8s %6d %8.2f %8.4f %8.2f %8.2f\n",
                        name, count(), mean(), stDev(), min(), max());
    }
  }
  
  // effect   Print on the system console a title line for statistics
  public static void statsTitles()
  {
    System.out.printf("  Name    Count     Mean    StDev      Min      Max\n");
  }
  
  // **********************
  // *                    *
  // *  Gray-Level Image  *
  // *                    *
  // **********************
  
  public class Image
  {
    private int[][] pixels;
    
    // returns  Width and height of the image
    public int width () { return pixels[0].length;}
    public int height() { return pixels.length;}
  
    // effect   Construct image of specified size, all pixels 0
    public Image(int width, int height)
    {
      pixels = new int[height][width];
    }
    
    // returns  Gray value of pixel at specified coordinate
    public int getPixel(int x, int y)
    {
      return pixels[y][x];
    }
    
    // returns  z
    // effect   Set gray value of pixel at specified coordinate to z
    public int setPixel(int x, int y, int z)
    {
      return pixels[y][x] = z;
    }
    
    // effect   Print image on system console, compressing the gray value
    //          range to 0 - 9.
    public void print()
    {
      // Compute range used
      Stats range = new Stats();
      for (int y = 0; y < height(); ++y)
        for (int x = 0; x < width(); ++x)
          range.add(getPixel(x, y));
      
      // Print image
      for (int y = 0; y < height(); ++y)
      {
        for (int x = 0; x < width(); ++x)
        {
          int z = 10 * (getPixel(x, y) - (int)range.min()) / (int)(range.max() - range.min() + 1);
          if (z > 0)
            System.out.printf("%2d", z);
          else
            System.out.printf(" .");
        }
        System.out.printf("\n");
      }
    }
  }
  
  // *********************************
  // *                               *
  // *  Syntheticly Rendered Shapes  *
  // *                               *
  // *********************************
  
  public interface Shape
  {
    double outside(int x, int y);
  }
  
  // Synthetic rounded rectangle
  public class RoundedRectangle implements Shape
  {
    private double x0, y0;            // center
    private double cs, sn;            // cos, sin of orientation
    private double xRadius, yRadius;  // rectangle radii
    private double cornerRadius, desiredCornerRadius;
    private double xc, yc;            // point at center of rounded corner
    
    // effect   Construct rounded rectangle of specified geometry
    public RoundedRectangle(double x0, double y0, double angle,
                            double xRadius, double yRadius,double cornerRadius)
    {
      setCenter(x0, y0);
      setRadii(xRadius, yRadius);
      setCornerRadius(cornerRadius);
      setAngle(angle);
    }
    
    // effect   Get/set center
    public double xCenter() { return x0;}
    public double yCenter() { return y0;}
    public void setCenter(double x, double y) { x0 = x; y0 = y;}
    
    // effect   Get/set angle
    public double angle() { return Math.atan2(sn, cs);}
    public void setAngle(double radians)
    {
      cs = Math.cos(radians);
      sn = Math.sin(radians);
    }
    
    // effect   Get/set radii
    public double xRadius() { return this.xRadius;}
    public double yRadius() { return this.yRadius;}
    public void setRadii(double rx, double ry)
    {
      xRadius = Math.max(rx, 1.0);
      yRadius = Math.max(ry, 1.0);
      setCorner();
    }
    
    // effect   Get/set corner radius
    public double cornerRadius() { return desiredCornerRadius;}
    public void setCornerRadius(double r)
    {
      desiredCornerRadius = r;
      setCorner();
    }
    
    // effect   Internal calculations when radii change
    private void setCorner()
    {
      cornerRadius = Math.min(desiredCornerRadius, Math.min(xRadius, yRadius));
      xc = xRadius - cornerRadius;
      yc = yRadius - cornerRadius;
    }
    
    // returns  Distance to edge, + for outside - for inside
    public double outside(int x, int y)
    {
      double u = Math.abs((x - x0) *  cs + (y - y0) * sn);
      double v = Math.abs((x - x0) * -sn + (y - y0) * cs);
      u -= xc;
      v -= yc;
      if (u > 0 && v > 0)
        return Math.sqrt(u * u + v * v) - cornerRadius;
      return (u >= v ? u : v) - cornerRadius;
    }
  }
  
  // ***********************
  // *                     *
  // *  Camera Parameters  *
  // *                     *
  // ***********************
  
  // Camera.acquire() will render all shapes put here
  public Vector<Shape> shapes = new Vector<Shape>();
  
  public double   edgeSigma   = 0.5;    // Edge model, can be negative or 0
  public double   noiseSigma  = 0.01;   // Standard deviation of gaussian noise, fraction of
                                        // range between blackLevel and whiteLevel
  public boolean  noiseEnable = false;  // Enable adding noise to acquired images
  public int      imageWidth  = 48;     // Width (pixels) of simulated camera sensor
  public int      imageHeight = 40;     // Height (pixels) of simulated camera sensor
  public int      blackLevel  = 64;     // Black (darkest) gray level
  public int      whiteLevel  = 192;    // White (lightest) gray level
  public Image    image;                // Last acquired image
  
  private Random noiseGenerator = new Random(0x5555555555555555L);
  
  // effect   Acquire an image as specified by above parameters
  public void acquire()
  {
    // Render all of the specified shapes into a floating point array, values in the
    // range [0..1], and using the edge model specified by edgeSigma.
    double[][] light = new double[imageHeight][imageWidth];
    for (int y = 0; y < imageHeight; ++y)
      for (int x = 0; x < imageWidth; ++x)
      {
        double z = 0;
        for (int s = 0; s < shapes.size(); ++s)
        {
          double a = shapes.get(s).outside(x, y);
          if (edgeSigma != 0)
          {
            a /= edgeSigma;
            if (a >= 6.0)
              a = edgeSigma > 0 ? 0 : 1;
            else
              a = 1.0 / (1.0 + Math.exp(a));
          }
          else
            a = a > 0 ? 0 : 1;
          z = Math.abs(z - a);
        }
        light[y][x] = z;
      }
   
    // Add noise if enabled
    if (noiseEnable)
    {
      for (int y = 0; y < imageHeight; ++y)
        for (int x = 0; x < imageWidth; ++x)
          light[y][x] += noiseSigma * noiseGenerator.nextGaussian();
    }
    
    // Digitize the image (convert from floating point light values to integer
    // gray values).
    image = new Image(imageWidth, imageHeight);
    for (int y = 0; y < imageHeight; ++y)
      for (int x = 0; x < imageWidth; ++x)
        image.setPixel(x, y, blackLevel + (int)(light[y][x] * (whiteLevel - blackLevel)));
  }

  // effect   Print on system console the camera parameters, using one line
  public void print()
  {
    System.out.printf("%.2f edge, ", edgeSigma);
    if (noiseEnable)
      System.out.printf("%5.2f%% noise, ", 100 * noiseSigma);
    else
      System.out.printf("no noise, ");
    System.out.printf("%dx%d image, %d black, %d white\n",
                      imageWidth, imageHeight, blackLevel, whiteLevel);
  }
}
