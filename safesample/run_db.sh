psql -f $1 test_sampling
start_time=$(gdate +%s%3N)
python query_parser.py --db test_sampling <<EOF
openworld
P(x1) R(x1,y1) Q(x2) S(x2,y2)
EOF

end_time=$(gdate +%s%3N)
elapsed_time=$(expr $end_time - $start_time)
echo "DB: $1" >> elapsed_time.log
echo "Elapsed: $elapsed_time" >> elapsed_time.log
