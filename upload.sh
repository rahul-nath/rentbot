for file in lib/aiml/*
do
  pb upload "$file"
done

for file in lib/maps/*
do
  pb upload "$file"
done

for file in lib/sets/*
do
  pb upload "$file"
done

for file in lib/substitutions/*
do
  pb upload "$file"
done

for file in lib/system/*
do
  pb upload "$file"
done
