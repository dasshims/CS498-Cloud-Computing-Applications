rm -rf ./TopTitlesClasses; rm -rf ./A-output; rm TopTitles.jar
mkdir ./TopTitlesClasses; \
javac -cp $(hadoop classpath) TopTitles.java -d TopTitlesClasses; \
jar -cvf TopTitles.jar -C TopTitlesClasses/ ./ ; \
hadoop jar TopTitles.jar TopTitles -D stopwords=stopwords.txt -D delimiters=delimiters.txt dataset/titles ./A-output


rm -rf ./TopTitleStatisticsClasses; rm -rf ./B-output; rm TopTitleStatistics.jar
mkdir ./TopTitleStatisticsClasses; \
javac -cp $(hadoop classpath) TopTitleStatistics.java -d TopTitleStatisticsClasses; \
jar -cvf TopTitleStatistics.jar -C TopTitleStatisticsClasses/ ./; \
hadoop jar TopTitleStatistics.jar TopTitleStatistics -D stopwords=stopwords.txt -D delimiters=delimiters.txt dataset/titles ./B-output


rm -rf ./OrphanPagesClasses; rm -rf ./C-output; rm OrphanPages.jar
mkdir ./OrphanPagesClasses; \
javac -cp $(hadoop classpath) OrphanPages.java -d OrphanPagesClasses; \
jar -cvf OrphanPages.jar -C OrphanPagesClasses/ ./ ; \
hadoop jar OrphanPages.jar OrphanPages dataset/links ./C-output

rm -rf ./TopPopularLinksClasses; rm -rf ./D-output; rm TopPopularLinks.jar
mkdir ./TopPopularLinksClasses; \
javac -cp $(hadoop classpath) TopPopularLinks.java -d TopPopularLinksClasses; \
jar -cvf TopPopularLinks.jar -C TopPopularLinksClasses/ ./ ; \
hadoop jar TopPopularLinks.jar TopPopularLinks dataset/links ./D-output


rm -rf ./PopularityLeagueClasses; rm -rf ./E-output; rm PopularityLeague.jar
mkdir ./PopularityLeagueClasses; \
javac -cp $(hadoop classpath) PopularityLeague.java -d PopularityLeagueClasses; \
jar -cvf PopularityLeague.jar -C PopularityLeagueClasses/ ./ ; \
hadoop jar PopularityLeague.jar PopularityLeague -D league=dataset/league.txt dataset/links ./E-output

rm -rf ./TopReviewsClasses; rm -rf ./F-output; rm TopReviews.jar
mkdir ./TopReviewsClasses; \
javac -cp "$(hadoop classpath)" TopReviews.java -d TopReviewsClasses; \
jar -cvf TopReviews.jar -C TopReviewsClasses/ ./ ; \
hadoop jar TopReviews.jar TopReviews -D stopwords=stopwords.txt -D delimiters=delimiters.txt dataset/yelp ./F-output


Part A: Congrats!_All_lines_are_correct!      ;
Part B: Congrats!_All_lines_are_correct!      ;
Part C: Invalid_output.The_number_of_lines_produced_by_your_code_is_not_valid.      ;
Part D: Congrats!_All_lines_are_correct!      ;
Part E: Congrats!_All_lines_are_correct!      ;
Part F: Invalid_output.The_number_of_lines_produced_by_your_code_is_not_valid.      ;






