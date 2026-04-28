for repo in $(cat repos-minus-MAM-basics.txt); do
    (echo ../$repo && cd .. && git clone git@github.com:bdenckla/$repo.git)
done

