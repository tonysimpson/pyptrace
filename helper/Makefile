
..pyptrace/const.py: const
	./const > ../pyptrace/const.py

const: const.c
	gcc const.c -o const

const.c: gen.sh
	sh gen.sh > const.c

clean:
	rm -rf const

.PHONY: clean
