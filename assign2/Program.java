package Vision;

public class Program
{
    // **********************************
    // *                                *
    // *  Utility Functions for Angles  *
    // *                                *
    // **********************************

    // Convert specified angle in degrees to equivalent angle in the range
    // [-90..90)
    public static double angleMod180(double x)
    {
        int n = (int)(x / 90.0);
        if (n >= 0)
            n = (n + 1) >> 1;
        else
            n >>= 1;
        if (x == -90.0)
            n = 0;
        return x - n * 180.0;
    }

    // Convert radians to degrees
    public static double degrees(double radians)
    {
        return radians * 180.0 / Math.PI;
    }

    // Convert degrees to radians
    public static double radians(double degrees)
    {
        return degrees * Math.PI / 180.0;
    }

    // ******************
    // *                *
    // *  Main Program  *
    // *                *
    // ******************

    public static void main(String[] args)
    {
        // Make a camera and synthetic shapes to make two blobs, one hollow with the
        // other inside.
        Camera camera = new Camera();
        camera.shapes.add(camera.new RoundedRectangle(24, 20, radians( 14), 18, 12, 4));
        camera.shapes.add(camera.new RoundedRectangle(24, 20, radians( 14), 14,  8, 3));
        camera.shapes.add(camera.new RoundedRectangle(26, 21, radians(-30),  5,  2, 2));

        // Acquire and print image
        camera.acquire();
        camera.image.print();
        camera.print();

        // Run blob analysis and print results
        Blob blob = new Blob();
        blob.run(camera.image);
        blob.thresh.print();
        blob.print();

        // Discard previous shapes and add new shapes to make one hollow blob. Using an
        // array of two shapes avoids lots of copy/paste programming, allows shape list
        // to be modified easily.
        camera.shapes.clear();
        Camera.RoundedRectangle[] shapes = new Camera.RoundedRectangle[2];
        shapes[0] = camera.new RoundedRectangle(24, 20,  0, 12.4, 6.2, 3);
        shapes[1] = camera.new RoundedRectangle(24, 20,  0,  6.2, 3.1, 2);
        for (int i = 0; i < shapes.length; ++i)
            camera.shapes.add(shapes[i]);

        // Acquire and print the image
        camera.acquire();
        System.out.printf("\n");
        camera.image.print();

        // Make statistics objects for six geometric blob properties. Using an
        // array avoids lots of copy/paste programming
        Camera.Stats[] stats = new Camera.Stats[6];
        for (int i = 0; i < stats.length; ++i)
            stats[i] = camera.new Stats();
        String[] names = {"Area", "xCenter", "yCenter", "Angle", "Length1", "Length2"};

        // Make a hard and fuzzy threshold for testing. Using an array allows other
        // thresholds to be added easily.
        Blob.Threshold[] thresholds = new Blob.Threshold[2];
        thresholds[0] = blob.new HardPosThreshold(128);
        thresholds[1] = blob.new FuzzyThreshold(96, 160);

        // Loop over the threshold types
        for (int t = 0; t < thresholds.length; ++t)
        {
            blob.thresh = thresholds[t];

            // Loop over the no noise/noise choice
            for (int n = 0; n < 2; ++n)
            {
                camera.noiseEnable = n != 0;

                // Clear all six statistics objects.
                for (int i = 0; i < stats.length; ++i)
                    stats[i].clear();

                // Loop over angles and translations
                for (double deg = 0; deg < 180; deg += 10)
                    for (double y = 20; y < 21; y += 0.1)
                        for (double x = 24; x < 25; x += 0.1)
                        {
                            // Set true position, orientation of rendered blob
                            for (int i = 0; i < shapes.length; ++i)
                            {
                                shapes[i].setCenter(x, y);
                                shapes[i].setAngle(radians(deg));
                            }

                            // Acquire image and run blob analysis
                            camera.acquire();
                            blob.run(camera.image);

                            // If we found a result, add to statistics
                            if (blob.results.size() > 0)
                            {
                                Blob.Result r = blob.results.get(0);
                                stats[0].add(r.area());
                                stats[1].add(r.xCenter() - x);
                                stats[2].add(r.yCenter() - y);
                                stats[3].add(angleMod180(degrees(r.angle()) - deg));
                                stats[4].add(r.principalLength1());
                                stats[5].add(r.principalLength2());
                            }
                        }

                        // Print statistics table
                        System.out.printf("\n");
                        camera.print();
                        blob.thresh.print();
                        Camera.statsTitles();
                        for (int i = 0; i < stats.length; ++i)
                            stats[i].print(names[i]);
                    }
                }
            }
        }
    }
}