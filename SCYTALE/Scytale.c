/******************************************************************************/
/*スキュタレー暗号を用いたエンコーダー、デコーダー。						  */
/*一周分に書ける文字数を指定し、祖の文字数に従って暗号文を作成する。また、暗号*/
/*文に対し暗号文の文字列長の約数でブルートフォースアタックを行う。			  */
/******************************************************************************/
/*関数の構成																  */
/*	main()																	  */
/*		メイン関数															  */
/*	Encoder()																  */
/*		入力文字列に対して、スキュタレーの一周分に書ける文字列数分だけ読み飛ば*/
/*		したものを暗号文として出力する関数。冗字として"*"を用い、"*"でパティン*/
/*		グされた二列を冗字列として付加する。								  */
/*	Decoderf()																  */
/*		入力文字列長の約数を考慮しその約数の場合についてブルートフォースアタッ*/
/*		クを実行する。														  */
/******************************************************************************/
#include<stdio.h>
#include<string.h>
#include<stdlib.h>

#define M 20
#define N 2048

void Encoder( void );
void Decoder( void );

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
	printf("#This program is encoder and decoder for Scytale chipher.  #\n");
	printf("#First character is regarded as initial of strings.	   #\n");
	printf("#About radius of scytale, \"R=n\" means \"Read a character at # \n");
	printf("#the (n-1)th here.                                         #\n");
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
			Encoder();
			break;
		case 'D' :
			Decoder();
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
/*	・変数dumyはscanf()実行時に"\n"がバッファ内に取り残され、次の入力受付に影 */
/*	　響を及ぼすのを防ぐために設定。										  */
/******************************************************************************/
void Encoder( void )
{
	system("clear");
	char *str;
	char dummy;
	int R, n, i, j;
	str = (char *)malloc(sizeof(char)*N);
	if( str==NULL )
	{
		exit(0);
	}
	printf("Enter radius  : "); scanf("%d%c", &R, &dummy);
	printf("Enter strings : ");	fgets( str , N , stdin );
	
	str[strlen(str)] = '\0';
	n = strlen(str)/R+0.9;
	if( ((n+1)%R)!=0 )
	{
		for( i=strlen(str)-1 ; i<(n+2)*R ; i++ )
		{
			str[i] = '*';
		}
	}
	n= strlen(str)/R+0.9;

	printf("Encode successed : ");
	for( i=0 ; i<R ; i++ )
	{
		for( j=0 ; j<n ; j++ )
		{
			if( str[i+(j*R)]=='\0' )
			{
				str[i+(j*R)]='@';
			}
			printf("%c", str[i+(j*R)]);
		}
	}
	putchar('\n');
	free(str);
}

/******************************************************************************/
/*注釈																		  */
/******************************************************************************/
/*																			  */
/******************************************************************************/
void Decoder( void )
{	
	system("clear");
	char *str;
	int n, i, j, k;
	str = (char *)malloc(sizeof(char)*N);
	if( str==NULL )
	{
		exit(0);
	}
	printf("Enter strings : ");	fgets( str , N , stdin );
	str[strlen(str)-1]='\0';

	printf("Decode successed\n");
	for( i=1 ; i<=strlen(str) ; i++ )
	{
		if( (strlen(str)%i)!=0 )
		{
			continue;
		}
		n = strlen(str)/i+0.9;
		printf("R=%2d : ", i);
		for( j=0 ; j<i ; j++ )
		{
			for( k=0 ; k<n ; k++ )
			{
				printf("%c", str[j+(i*k)]);
			}
		}
		putchar('\n');
	}

	free(str);
}

