import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Collections;
import java.util.List;
import java.util.StringTokenizer;
import java.util.TreeSet;

public class TopReviews extends Configured implements Tool {
    public static final Log LOG = LogFactory.getLog(TopReviews.class);

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new Configuration(), new TopReviews(), args);
        System.exit(res);
    }

    @Override
    public int run(String[] args) throws Exception {
        Configuration conf = this.getConf();

        FileSystem fs = FileSystem.get(conf);
        Path tmpPath = new Path("./preF-output");

        Job jobA = Job.getInstance(conf, "Top Reviews Job A");
        jobA.setJarByClass(TopReviews.class);

        jobA.setMapperClass(ReviewCountMap.class);
        jobA.setReducerClass(ReviewCountReduce.class);

        jobA.setOutputKeyClass(Text.class);
        jobA.setOutputValueClass(IntWritable.class);

        FileInputFormat.setInputPaths(jobA, new Path(args[0]));
        FileOutputFormat.setOutputPath(jobA, tmpPath);

        boolean successA = jobA.waitForCompletion(true);

        if (!successA) {
            System.err.println("Job A failed, exiting");
            return 1;
        }
        System.out.println("Job A Finished, starting job B...");

        Job jobB = Job.getInstance(conf, "Top Reviews Job B");
        jobB.setJarByClass(TopReviews.class);

        jobB.setMapperClass(TopReviewsMap.class);
        jobB.setReducerClass(TopReviewsReduce.class);

        jobB.setMapOutputKeyClass(NullWritable.class);
        jobB.setMapOutputValueClass(TextArrayWritable.class);

        jobB.setOutputKeyClass(Text.class);
        jobB.setOutputValueClass(NullWritable.class);

        FileInputFormat.setInputPaths(jobB, tmpPath);
        FileOutputFormat.setOutputPath(jobB, new Path(args[1]));

        boolean successB = jobB.waitForCompletion(true);

        return successB ? 0 : 1;
    }

    public static String readHDFSFile(String path, Configuration conf) throws IOException{
        Path pt=new Path(path);
        FileSystem fs = FileSystem.get(pt.toUri(), conf);
        FSDataInputStream file = fs.open(pt);
        BufferedReader buffIn=new BufferedReader(new InputStreamReader(file));

        StringBuilder everything = new StringBuilder();
        String line;
        while( (line = buffIn.readLine()) != null) {
            everything.append(line);
            everything.append("\n");
        }
        return everything.toString();
    }

    public static class TextArrayWritable extends ArrayWritable {
        public TextArrayWritable() {
            super(Text.class);
        }

        public TextArrayWritable(String[] strings) {
            super(Text.class);
            Text[] texts = new Text[strings.length];
            for (int i = 0; i < strings.length; i++) {
                texts[i] = new Text(strings[i]);
            }
            set(texts);
        }
    }

    public static class ReviewCountMap extends Mapper<Object, Text, Text, IntWritable> {
        List<String> stopWords;
        String delimiters;

        @Override
        protected void setup(Context context) throws IOException,InterruptedException {

            Configuration conf = context.getConfiguration();

            String stopWordsPath = conf.get("stopwords");
            String delimitersPath = conf.get("delimiters");

            this.stopWords = Arrays.asList(readHDFSFile(stopWordsPath, conf).split("\n"));
            this.delimiters = readHDFSFile(delimitersPath, conf);
        }

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            //Calculate scores and pass along with business_id to the reducer
            //context.write(new Text(business_id), new IntWritable(weight * stars));
            try {
                JSONObject obj = new JSONObject(value.toString());
                String business_id = obj.getString("business_id");
                int stars = obj.getInt("stars");
                String text = obj.getString("text").toLowerCase();

                //System.out.println("business_id -- "+business_id + " \nstart -- "+stars+" \ntext"+text);

                // Adjust stars to range (-2 to 2)
                int adjustedStars = stars - 3;

                StringTokenizer tokenizer = new StringTokenizer(text, delimiters);
                int reviewLength = 0;
                while (tokenizer.hasMoreTokens()) {
                    String token = tokenizer.nextToken();
                    if (!stopWords.contains(token)) {
                        reviewLength++;
                    }
                }

                // Calculate weight * stars
                int weight = reviewLength; // Using review length as weight
                //System.out.println("business_id -- "+business_id+ " has adjustedStars -- "+adjustedStars + " and weight -- "+weight);
                //System.out.println("Calculated weight == "+adjustedStars * weight);
                context.write(new Text(business_id), new IntWritable((int) (adjustedStars * weight)));

            } catch (JSONException e) {
                // JSON parsing error
                e.printStackTrace();
            }
        }
    }

    public static class ReviewCountReduce extends Reducer<Text, IntWritable, Text, DoubleWritable> {
        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            //Output average scores
            int sum = 0;
            int numReviews = 0;

            // Calculate sum of adjusted stars and total number of reviews
            for (IntWritable value : values) {
                sum += value.get();
                numReviews++;
            }

            // Calculate average score
            double averageScore = (double) sum / numReviews;
            context.write(key, new DoubleWritable(averageScore));
        }
    }

//    public static class TopReviewsMap extends Mapper<Object, Text, Text, IntWritable> {
    public static class TopReviewsMap extends Mapper<LongWritable, Text, NullWritable, TextArrayWritable> {

        private TreeSet<Pair<Double, String>> countToReviewMap = new TreeSet<Pair<Double, String>>();
        Integer N;

        @Override
        protected void setup(Context context) throws IOException,InterruptedException {
            Configuration conf = context.getConfiguration();
            this.N = conf.getInt("N", 10);
        }

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        //public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            //Calculate weighted review score for each business ID, keeping the count of map <=N
            String line = value.toString();
            String[] parts = line.split("\t"); // Assuming tab-separated input
            //System.out.println("line -- "+line);

            if (parts.length == 2) {
                String businessId = parts[0];
                //int weightedReviewScore = Integer.parseInt(parts[1]);
                double weightedReviewScore = Double.parseDouble(parts[1]);

                // Add the pair of weighted review score and business ID to the TreeSet
                countToReviewMap.add(new Pair<>(weightedReviewScore, businessId));

                // Keep only top N elements in the TreeSet
                if (countToReviewMap.size() > this.N) {
                    countToReviewMap.pollFirst();
                }
            }
            System.out.println("parts length "+parts.length);
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            //output the entries of the map
            //context.write(NullWritable.get(), entry);
            for (Pair<Double, String> pair : countToReviewMap) {
                System.out.println("Pair first " + pair.first);
                System.out.println("Pair second " + pair.second);
                String[] strings = {pair.second, pair.first.toString()};
                TextArrayWritable val = new TextArrayWritable(strings);
                context.write(NullWritable.get(), val);
            }

        }
    }

    public static class TopReviewsReduce extends Reducer<NullWritable, TextArrayWritable, Text, NullWritable> {
        private TreeSet<Pair<Double, String>> countToReviewMap = new TreeSet<Pair<Double, String>>();
        Integer N;

        @Override
        protected void setup(Context context) throws IOException,InterruptedException {
            Configuration conf = context.getConfiguration();
            this.N = conf.getInt("N", 10);
        }

        @Override
        public void reduce(NullWritable key, Iterable<TextArrayWritable> values, Context context) throws IOException, InterruptedException {
            //TODO - output top 10 business_id
            //context.write(business_id, NullWritable.get());
            for (TextArrayWritable val : values) {
                //Text[] pair = (Text[]) val.toArray();
                Writable[] pair = val.get();
                String businessId = pair[0].toString();
                double weightedReviewScore = Double.parseDouble(pair[1].toString());
                System.out.println("business id inside reducer -- "+businessId);
                System.out.println("weighted review score inside reducer -- "+weightedReviewScore);
                // Add the pair of weighted review score and business ID to the TreeSet
                countToReviewMap.add(new Pair<>(weightedReviewScore, businessId));

                // Keep only top N elements in the TreeSet
                if (countToReviewMap.size() > this.N) {
                    countToReviewMap.pollFirst();
                }
            }

            // Output the top N business IDs with the highest weighted review scores in descending order
            int rank = 1;
            while (!countToReviewMap.isEmpty()) {
                Pair<Double, String> pair = countToReviewMap.pollLast();
                context.write(new Text(pair.second), NullWritable.get());
                rank++;
            }
        }
    }
}

class Pair<A extends Comparable<? super A>,
    B extends Comparable<? super B>>
    implements Comparable<Pair<A, B>> {

    public final A first;
    public final B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    public static <A extends Comparable<? super A>,
        B extends Comparable<? super B>>
    Pair<A, B> of(A first, B second) {
        return new Pair<A, B>(first, second);
    }

    @Override
    public int compareTo(Pair<A, B> o) {
        int cmp = o == null ? 1 : (this.first).compareTo(o.first);
        return cmp == 0 ? (this.second).compareTo(o.second) : cmp;
    }

    @Override
    public int hashCode() {
        return 31 * hashcode(first) + hashcode(second);
    }

    private static int hashcode(Object o) {
        return o == null ? 0 : o.hashCode();
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Pair))
            return false;
        if (this == obj)
            return true;
        return equal(first, ((Pair<?, ?>) obj).first)
            && equal(second, ((Pair<?, ?>) obj).second);
    }

    private boolean equal(Object o1, Object o2) {
        return o1 == o2 || (o1 != null && o1.equals(o2));
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ')';
    }
}