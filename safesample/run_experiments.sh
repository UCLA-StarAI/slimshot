for n in 10 20 40 80 160 320 640 1280 2560 5120 10240; do
    python generate_data.py $n 2 2 generated_data/size_$n.sql
    psql -f generated_data/size_$n.sql test_sampling
    start_time=$(gdate +%s%3N)
    psql -d test_sampling -f sql_query.sql
    end_time=$(gdate +%s%3N)
    elapsed_time=$(expr $end_time - $start_time)
    echo "DB: $n" >> elapsed_time.log
    echo "Elapsed: $elapsed_time" >> elapsed_time.log
done

