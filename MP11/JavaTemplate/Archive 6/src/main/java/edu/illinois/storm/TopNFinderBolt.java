package main.java.edu.illinois.storm;

import java.util.HashMap;
import java.util.Map;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;
import static java.lang.System.currentTimeMillis;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

/**
 * a bolt that finds the top n words.
 */
public class TopNFinderBolt extends BaseRichBolt {
    private OutputCollector collector;
    private HashMap<String, Integer> currentTopWords = new HashMap<String, Integer>();

    private int N;
    private static final long INTERVALTOREPORT = 2;
    private long lastReportTime = currentTimeMillis();

    // Hint: Add necessary instance variables and inner classes if needed

    public TopNFinderBolt(int N) {
        this.N = N;
    }


    @Override
    public void prepare(Map conf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
    }

    public TopNFinderBolt withNProperties(int N) {
    /* ----------------------TODO-----------------------
    Task: set N
    ------------------------------------------------- */
        this.N = N;
        return this;
    }

    @Override
    public void execute(Tuple tuple) {
    /* ----------------------TODO-----------------------
    Task: keep track of the top N words
		Hint: implement efficient algorithm so that it won't be shutdown before task finished
		      the algorithm we used when we developed the auto-grader is maintaining a N size min-heap
    ------------------------------------------------- */

        String word = tuple.getString(0);
        Integer count = tuple.getInteger(1);
        System.out.println("word "+word+" is with count "+count);
        if(word == "" || word == null)
            System.out.println("Empty word ::: "+word);
        else {
            if (currentTopWords.size() <= N) {
                currentTopWords.put(word, count);
            } else {
                removeLowest();
                currentTopWords.put(word, count);
            }
        }

        collector.emit(new Values(printMap()));

        //reports the top N words periodically
        /*System.out.println("Last reported time diff ::: "+(currentTimeMillis() - lastReportTime));
        if (currentTimeMillis() - lastReportTime >= INTERVALTOREPORT) {
            System.out.println("Emitting new");
            collector.emit(new Values(printMap()));
            lastReportTime = currentTimeMillis();
        }*/
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
    /* ----------------------TODO-----------------------
    Task: define output fields
		Hint: there's no requirement on sequence;
					For example, for top 3 words set ("hello", "word", "cs498"),
					"hello, world, cs498" and "world, cs498, hello" are all correct
    ------------------------------------------------- */

        declarer.declare(new Fields("top-N"));
    }

    private void removeLowest() {
        String keyWithLowestVal = null;
        Integer lowestVal = null;
        for (Map.Entry<String, Integer> each : currentTopWords.entrySet()) {
            if (lowestVal == null || each.getValue() < lowestVal) {
                keyWithLowestVal = each.getKey();
                lowestVal = each.getValue();
            }
        }
        currentTopWords.remove(keyWithLowestVal);
    }

    public String printMap() {
        StringBuilder stringBuilder = new StringBuilder();
        //stringBuilder.append("top-words = [ ");
        for (String word : currentTopWords.keySet()) {
            System.out.println("currentTopWords ::: "+currentTopWords);
            stringBuilder.append(word).append(", ");
        }
        int lastCommaIndex = stringBuilder.lastIndexOf(",");
        //stringBuilder.deleteCharAt(lastCommaIndex + 1);
        //stringBuilder.deleteCharAt(lastCommaIndex);
        //stringBuilder.append("]");
        return stringBuilder.toString();
    }

}
