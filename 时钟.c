#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <Windows.h>
#define UTC (+8)
#define A 'O'
#define B ' '
#define SLEEP_TIME 500
// static int count;
char Matrix[7][33] = {
	{'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O'},
	{'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O'},
	{'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O'},
	{'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O'},
	{'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O'},
	{'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', 'O', ' ', ' ', 'O'},
	{'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ' ', ' ', ' ', 'O', 'O', 'O', 'O', ' ', 'O', 'O', 'O', 'O'} };

void printMatrix()
{
	for (int i = 0; i < 7; ++i)
	{
		for (int j = 0; j < 33; ++j)
			printf("%c", Matrix[i][j]);
		printf("\n");
	}
	// count++;
}

int ds, H, h, M, m, S, s;

void getTime()
{
	ds = time(NULL) % 86400;
	H = ((ds / 3600 + UTC)+24) % 24 / 10;
	h = ((ds / 3600 + UTC)+24)% 24 % 10;
	M = ds % 3600 / 60 / 10;
	m = ds % 3600 / 60 % 10;
	S = ds % 3600 % 60 / 10;
	s = ds % 3600 % 60 % 10;
}

int colOffset[] = { 0, 5, 12, 17, 24, 29 };

void writeRow(int row, int type, int ofst)
{
	switch (type)
	{
#define writeCol(c0, c1, c2, c3)               \
	{                                          \
		Matrix[row][0 + colOffset[ofst]] = c0; \
		Matrix[row][1 + colOffset[ofst]] = c1; \
		Matrix[row][2 + colOffset[ofst]] = c2; \
		Matrix[row][3 + colOffset[ofst]] = c3; \
	}
	case 1:
		writeCol(A, A, A, A) break;
	case 2:
		writeCol(A, B, B, B) break;
	case 3:
		writeCol(B, B, B, A) break;
	case 4:
		writeCol(A, B, B, A) break;
	}
}

void saveTime2Matrix()
{
	int timeNumber[] = { H, h, M, m, S, s };
	for (int ofst = 0; ofst < 6; ++ofst)
	{
		switch (timeNumber[ofst])
		{
#define writeRowByType(type0, type1, type2, type3, type4, type5, type6) \
	{                                                                   \
		writeRow(0, type0, ofst);                                       \
		writeRow(1, type1, ofst);                                       \
		writeRow(2, type2, ofst);                                       \
		writeRow(3, type3, ofst);                                       \
		writeRow(4, type4, ofst);                                       \
		writeRow(5, type5, ofst);                                       \
		writeRow(6, type6, ofst);                                       \
	}
		case 1:
			writeRowByType(3, 3, 3, 3, 3, 3, 3) break;
			/* 0 1 2 3
			**********
			0|       A
			1|       A
			2|       A
			3|       A
			4|       A
			5|       A
			6|       A
			**********/
		case 2:
			writeRowByType(1, 3, 3, 1, 2, 2, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1|       A
			2|       A
			3| A A A A
			4| A
			5| A
			6| A A A A
			**********/
		case 3:
			writeRowByType(1, 3, 3, 1, 3, 3, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1|       A
			2|       A
			3| A A A A
			4|       A
			5|       A
			6| A A A A
			**********/
		case 4:
			writeRowByType(4, 4, 4, 1, 3, 3, 3) break;
			/* 0 1 2 3
			**********
			0| A     A
			1| A     A
			2| A     A
			3| A A A A
			4|       A
			5|       A
			6|       A
			**********/
		case 5:
			writeRowByType(1, 2, 2, 1, 3, 3, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1| A
			2| A
			3| A A A A
			4|       A
			5|       A
			6| A A A A
			**********/
		case 6:
			writeRowByType(1, 2, 2, 1, 4, 4, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1| A
			2| A
			3| A A A A
			4| A     A
			5| A     A
			6| A A A A
			**********/
		case 7:
			writeRowByType(1, 3, 3, 3, 3, 3, 3) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1|       A
			2|       A
			3|       A
			4|       A
			5|       A
			6|       A
			**********/
		case 8:
			writeRowByType(1, 4, 4, 1, 4, 4, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1| A     A
			2| A     A
			3| A A A A
			4| A     A
			5| A     A
			6| A A A A
			**********/
		case 9:
			writeRowByType(1, 4, 4, 1, 3, 3, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1| A     A
			2| A     A
			3| A A A A
			4|       A
			5|       A
			6| A A A A
			**********/
		case 0:
			writeRowByType(1, 4, 4, 4, 4, 4, 1) break;
			/* 0 1 2 3
			**********
			0| A A A A
			1| A     A
			2| A     A
			3| A     A
			4| A     A
			5| A     A
			6| A A A A
			**********/
		}
	}
}

int main()
{
	while (1)
	{
		getTime();
		saveTime2Matrix();
		printMatrix(); // printf("%d",count++);
		Sleep(SLEEP_TIME);
		system("cls");
	}
}
