package Vision;

import java.util.Stack;
import java.util.Vector;

public class Blob
{
    // *****************
    // *               *
    // *  Blob Result  *
    // *               *
    // *****************
    public class Result
    {
        // effect   Add one pixel to blob of specified weight and position
        public void add(double w, double x, double y)
        {
        }

        // returns  Blob area
        public double area()
        {
            return 0;
        }

        // returns  x coordinate of center of mass
        public double xCenter()
        {
            return 0;
        }

        // returns  y coordinate of center of mass
        public double yCenter()
        {
            return 0;
        }

        // returns  Angle in radians of first principal axis of inertia
        public double angle()
        {
            return 0;
        }

        // returns  First principal length
        double principalLength1()
        {
            return 0;
        }

        // returns  Second principal length
        public double principalLength2()
        {
            return 0;
        }
    }

    // ****************
    // *              *
    // *  Thresholds  *
    // *              *
    // ****************
    //
    // A Threshold is an object that can convert a raw value into a weight
    // in the range [0..1]
    public interface Threshold
    {
        // returns  The weight corresponding to the specified raw value
        double weight(double x);

        // effect   Print the threshold value to the system console
        void print();
    }

    // Hard positive threshold
    public class HardPosThreshold implements Threshold
    {
        public double threshold;

        public HardPosThreshold(double t)
        {
            threshold = t;
        }

        @Override
        public double weight(double x)
        {
            return x >= threshold ? 1.0 : 0.0;
        }

        public void print()
        {
            System.out.printf("Hard Threshold >= %.1f\n", threshold);
        }
    }

    // Hard negative threshold
    public class HardNegThreshold implements Threshold
    {
        public double threshold;

        public HardNegThreshold(double t)
        {
            threshold = t;
        }

        @Override
        public double weight(double x)
        {
            return x <= threshold ? 1.0 : 0.0;
        }

        public void print()
        {
            System.out.printf("Hard Threshold <= %.1f\n", threshold);
        }
    }

    // Linear fuzzy threshold
    public class FuzzyThreshold implements Threshold
    {
        public double t0, t1;

        public FuzzyThreshold(double t0, double t1)
        {
            this.t0 = t0;
            this.t1 = t1;
        }

        @Override
        public double weight(double x)
        {
            return Math.min(Math.max((x - t0) / (t1 - t0), 0.0), 1.0);
        }

        public void print()
        {
            System.out.printf("Fuzzy Threshold %.1f, %.1f\n", t0, t1);
        }
    }

    // *********************
    // *                   *
    // *  Blob Parameters  *
    // *                   *
    // *********************

    // Results go here
    public Vector<Result> results = new Vector<Result>();

    // run uses this threshold
    public Threshold thresh = new HardPosThreshold(128);

    // Blobs smaller (lighter) than this are discarded.
    public double minArea = 8;

    // ***********************
    // *                     *
    // *  Run Blob Analysis  *
    // *                     *
    // ***********************
    //
    // Run blob analysis on specified image and place results in the above vector.
    // This is where all connectivity analysis is done. Use above parameters.
    public void run(Camera.Image img)
    {
    }

    // effect   Print all results on system console.
    public void print()
    {
        System.out.printf("Id   Area     Center    Angle Principal Len\n");
        for (int i = 0; i < results.size(); ++i)
        {
            Result r = results.get(i);
            System.out.printf("%2d %6.1f (%5.1f,%5.1f) %5.1f  %5.1fx%5.1f\n",
                i, r.area(), r.xCenter(), r.yCenter(),
                r.angle() * 180 / Math.PI, 
                r.principalLength1(), r.principalLength2());      
        }
    }
}