package Vision;

import java.util.Stack;
import java.util.Vector;

public class Blob
{
    // ****
    // Point class
    // I've chosen to implement this myself rather than using a class like java.awt.Point
    // because I'd like to be able to handle the weight of the point internally within the Point class
    // ****
    public class Point {
        private double weight;
        private double x;
        private double y;

        public Point(double weight, double x, double y) {
            this.weight = weight;
            this.x = x;
            this.y = y;
        }

        // This class can also serve as a java.awt.Point replacement when weight is not specified.
        public Point(double x, double y) {
            this.weight = 0;
            this.x = x;
            this.y = y;
        }

        public double weight(){
            return this.weight;
        }

        public double x(){
            return this.x;
        }

        public double y(){
            return this.y;
        }
    }

    // *****************
    // *               *
    // *  Blob Result  *
    // *               *
    // *****************
    public class Result
    {
        public Stack<Point> stack = new Stack<Point>();
        public Stack<Point> blob = new Stack<Point>();

        public Boolean stack_empty() {
            return stack.empty();
        }

        public Point stack_pop() {
            return stack.pop();
        }

        public void stack_push(Point p) {
            stack.push(p);
        }

        // effect   Add one pixel to blob of specified weight and position
        public void add(double w, double x, double y)
        {
            Point newPoint = new Point(w, x, y);
            blob.push(newPoint);
        }

        // Function to handle calculation of area and COM in X and Y
        // Grouped in this way because the code for those three functions was very redundant 
        public Point geom_data(){
            // Copy the blob stack so as to not destroy data when popping
            Stack<Point> blob_copy = new Stack<Point>();
            blob_copy.addAll(blob);

            double area = 0;
            double COM_x = 0;
            double COM_y = 0;

            while (!blob_copy.empty()){
                Point point = blob_copy.pop();
                area += point.weight();
                COM_x += point.x() * point.weight();
                COM_y += point.y() * point.weight();
            }

            COM_x = COM_x / area;
            COM_y = COM_y / area; 

            return new Point(area, COM_x, COM_y);
        }

        // returns  Blob area
        public double area()
        {
            return geom_data().weight();
        }

        // returns  x coordinate of center of mass
        public double xCenter()
        {
            return geom_data().x();
        }

        // returns  y coordinate of center of mass
        public double yCenter()
        {
            return geom_data().y();
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

    // Current "result" (the blob being worked on) goes here
    Result current_result = new Result();

    // run uses this threshold
    public Threshold thresh = new HardPosThreshold(128);

    // Blobs smaller (lighter) than this are discarded.
    public double minArea = 8;

    // boolean array to track pixel visitation
    public Vector<Vector<Boolean>> mark = new Vector<Vector<Boolean>>();

    // Setter for Results vector
    public void results_add(Result r){
        results.add(r);
    }

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
        results.clear(); // per Bill's email, we must clear the results vector to prevent stats bugs

        // initialize mark array 2 larger than the image (for 1 px wide border)
        int expanded_height = img.height() + 2;
        int expanded_width = img.width() + 2;

        for(int j = 0; j < expanded_height; j++) {
            mark.insertElementAt(new Vector<Boolean>(), j);
            
            for(int i = 0; i < expanded_width; i++) {
                // if the point lies along any of the four edges of the mark array, mark it true (visited)
                if (i == 0 || i == expanded_width - 1 || j == 0 || j == expanded_height - 1) {
                    mark.elementAt(j).insertElementAt(Boolean.TRUE, i);
                }
                // if the point is not along an edge, mark it false (OK to visit)
                else {
                    mark.elementAt(j).insertElementAt(Boolean.FALSE, i);
                }
            }
        }

        // create a new blob object, the current one to be explored
        current_result = new Result();

        // For each pixel in the image
        for(int j = 0; j < img.height(); j++){
            for(int i = 0; i < img.width(); i++){
                // explore the pixel at (i, j)
                Boolean was_pushed = explore(i, j, img);

                // if the pixel was determined to be part of an object
                if (was_pushed) {
                    do {
                        Point popped_point = current_result.stack_pop();

                        // explore all the neighbors of popped_point
                        // "neighbors" is defined as 8-neighbor: E, NE, N, NW, W, SW, S, SE
                        for (int k = (int)popped_point.y()-1; k <= (int)popped_point.y() + 1; k++) {
                            for (int l = (int)popped_point.x()-1; l <= (int)popped_point.x() + 1; l++) {
                                // explore all neighbors but the self
                                if (!(l == (int)popped_point.x() && k == (int)popped_point.y())) {
                                    explore(l, k, img);
                                }
                            }
                        }
                    } while (!current_result.stack_empty());

                    if (current_result.area() > 20) {
                        results.add(current_result);
                    }

                    // reinitialize the blob object for the next go around
                    current_result = new Result();
                }
            }
        }
    }


    public Boolean explore(int i, int j, Camera.Image img) {
        if (mark.elementAt(j+1).elementAt(i+1) == Boolean.FALSE) {
            // Mark this pixel as having been visited
            mark.elementAt(j+1).setElementAt(Boolean.TRUE, i+1);

            // use a threshold to get the weight of the pixel
            double weight = thresh.weight(img.getPixel(i, j));

            // the pixel has been classified as "object" 
            if (weight >= 0.5) {
                // add the pixel to the last(current) results object 
                current_result.add(weight, i, j);
                current_result.stack_push(new Point(i, j));
                return Boolean.TRUE;
            }
        }
        return Boolean.FALSE;
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

    // effect  Print the "mark" (boolean visitation) vector to console.
    public void print_mark_vector() {
        for (Vector<Boolean> row : mark) {
            for (Boolean point : row) {
                if (point == Boolean.TRUE)
                    System.out.print("1 ");
                else if (point == Boolean.FALSE)
                    System.out.print("0 ");
            }
            System.out.println();
        }
    }
}