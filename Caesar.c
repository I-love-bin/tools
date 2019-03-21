/******************************************************************************/
/*シーザー暗号を用いたエンコーダー、デコーダー。							  */
/*エンコードしたい文字列に対してROT1~ROT25でエンコードした結果を表示し、デコー*/
/*ドしたい文字列に対してROT1~ROT25でデコードした結果を表示する。			  */
/******************************************************************************/
/*関数の構成																  */
/*	main()																	  */
/*		メイン関数															  */
/*	coder()																	  */
/*		文字列をエンコード、デコードする関数。main()でエンコーダーモードかデコ*/
/*		ーダーモードかの選択を行うが、どっちを選ぼうが同じである。			  */
/******************************************************************************/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define N 2048
#define M 20

void coder( void );

/******************************************************************************/
/*注釈																		  */
/******************************************************************************/
/*	・変数dumyはscanf()実行時に"\n"がバッファ内に取り残され、次の入力受付に影 */
/*	　響を及ぼすのを防ぐために設定。										  */
/******************************************************************************/
int main(void)
{
	char *choise;
	char dumy;
	choise = (char *)malloc(sizeof(char)*M);
	if( choise==NULL )
	{
		exit(0);
	}

	printf("############################################################\n");
	printf("#This program is encoder and decoder for Caesar chipher.   #\n");
	printf("#Spesial character like\"?\" and numbers wonn't be coded     #\n");
	printf("#This program shifts left to right.                        #\n");
	printf("############################################################\n");
	printf("\nE...Encoder mode\n");
	printf("D...Decoder mode\n");
	printf("Q...Quit a program\n");
	printf("Your choise : ");	scanf("%s%c", choise, &dumy);
	switch (*choise)
	{
		default :
			printf("This program only accept \"E\",\"D\"and\"Q\"\n");
			break;
		case 'E' :
			coder();
			break;
		case 'D' :
			coder();
			break;
		case 'Q' :
			printf("Quit a program\n");
			break;
	}
	free(choise);
	return(0);
}

/******************************************************************************/
/*注釈																		  */
/******************************************************************************/
/*																			  */
/******************************************************************************/
void coder( void )
{
	system("clear");
	char *str;
	int i , j;
	str = (char *)malloc((sizeof(char)*N));
	if( str==NULL )
	{
		exit(0);
	}
	printf("Enter strings : "); fgets( str , N , stdin );
	str[strlen(str)-1] = '\0';
	printf("At first... : %s\n", str);
	for( i=1 ; i<=26 ; i++ )
	{
		printf("ROT%2d : ", i);
		for( j=0 ; str[j]!='\0' ; j++ )
		{
			if( (65<=(int)str[j])&&((int)str[j]<=90)&&(90<((int)str[j]+1)) )
			{
				str[j] = (char)(((int)str[j]+1)-26);
			}
			else if( ((97<=(int)str[j])&&((int)str[j]<=122))&&(123<=((int)str[j]+1)) )
			{
				str[j] = (char)(((int)str[j]+1)-26);
			}
			else if( ((32<=(int)str[j])&&((int)str[j]<=64))||
					((91<=(int)str[j])&&((int)str[j]<=96))||
					((123<=(int)str[j])&&((int)str[j]<=126)) )
			{
				str[j]=str[j];
			}							
			else
			{
				str[j] = (char)((int)str[j]+1);
			}
			printf("%c", str[j]);
		}
		putchar('\n');
	}
	free(str);
}
