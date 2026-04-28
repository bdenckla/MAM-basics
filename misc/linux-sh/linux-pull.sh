for repo in $(cat repos.txt); do
    (echo ../$repo && cd ../$repo && git pull)
done

