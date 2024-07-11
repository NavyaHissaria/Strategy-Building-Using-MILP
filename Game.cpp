#include <iostream>
#include <fstream>
#include <cassert>
using namespace std;

int War(int enemy, int your)
{
  cout<<"Fight:"<<endl<<enemy<<" vs "<<your<<endl;
  if( enemy > your ) return -1;
  if( your >= enemy && (5 * enemy)/4 > your ) return your - (1 * enemy)/1;
  if( your >= (5 * enemy)/4 &&  (3 * enemy)/2 > your ) return your - (4 * enemy)/5;
  if( your >= (3 * enemy)/2 && (7 * enemy)/4 > your ) return your - (2 * enemy)/3;
  if( your >= (7 * enemy)/4 && 2 * enemy > your ) return your - (4 * enemy)/7;
  if( your >= (2 * enemy) && 3 * enemy > your ) return your - (1 * enemy)/2;
  if( your >= (3 * enemy) && 5 * enemy > your ) return your - (1 * enemy)/3;
  
  return your;
}

int main()
{
  std::cout<<"Give The Enemy File"<<std::endl;
  std::string enemyfile;
  std::cin >> enemyfile;

  std::cout<<"Give The Villager-Job File"<<std::endl;
  std::string Villagersfile;
  std::cin >> Villagersfile;

  std::ifstream EnemyArmy(enemyfile);
  if( EnemyArmy.is_open() == 0 ){ std::cout<<"Error Opening Enemy File"<<std::endl; return 0;}

  std::ifstream Jobs(Villagersfile);
  if( Jobs.is_open() == 0 ){ std::cout<<"Error Opening Jobs File"<<std::endl; return 0;}
   
  int T = 2500;
  int Cg = 10;
  int Cf = 10;
  int Ct = 10;
  int Tg = 30;
  int Tf = 40;
  //one job is defined as of 10-12 second.
  std::cout<<"Enter The Initial Army"<<std::endl;
  int Currarmy ; 
  std::cin >> Currarmy;
  int hitpoint = 72;
  
  //initially we have 24 soldiers.

  int gold = 820 - 75;
  int food = 1020;
  
  int Treasure = 0;
  //some inital wood is requierd for making houses so assume that the availble jobs are reduced.
   int wave = 0;
  while(1)
  { wave = wave + 1;
    std::string line;
    std::getline(EnemyArmy, line);
    int enemyarmy = std::stoi(line);
    
    std::cout<<"---------Upcoming Wave: "<<wave<<"----------"<<std::endl;
    std::cout<<"Upcoming Enemy Strength: "<<enemyarmy<<std::endl;
   
    std::getline(Jobs, line);
    int jobs = std::stoi(line);
    
    std::cout<<"Availble villager's jobs: "<<jobs<<std::endl;

    int jobsforg;
    int jobsforf;
    int jobsforT;
    std::cout<<"Present Situation is: "<<std::endl;
    std::cout<<"Gold: "<<gold<<std::endl;
    std::cout<<"Food: "<<food<<std::endl;
    std::cout<<"Treasure: "<<Treasure<<std::endl;

Decide:
    
    std::cout<<"No. Of Jobs for Gold: ";
    
    std::cin>>jobsforg;
    std::cout<<std::endl;

    if( jobsforg > jobs ){std::cout<<"Invalid"<<std::endl; goto Decide;}
    
    std::cout<<"No. Of Jobs for Food: ";
    std::cin >> jobsforf;
    if( jobsforg + jobsforf > jobs){std::cout<<"Invalid"<<std::endl; goto Decide;}
    
    jobsforT = jobs - (jobsforg + jobsforf);
    assert(jobsforT >= 0);
    
    gold = gold + jobsforg * Cg;
    food = food + jobsforf * Cf;
    Treasure = Treasure + jobsforT * Ct;
    
    std::cout<<"You Have This Much"<<std::endl;
    std::cout<<"Gold: "<<gold<<std::endl;
    std::cout<<"Food: "<<food<<std::endl;
    std::cout<<"Treasure: "<<Treasure<<std::endl;
    std::cout<<"Army: "<<Currarmy<<std::endl;
    
    if( Treasure >= T ){std::cout<<"You Are Victorious"<<std::endl; return 0;}

    int train=0;
train2:

    std::cout<<"How Much You Want To Train: ";
    std::cin>>train;
    if(train * Tg > gold || train * Tf > food ){ std::cout<<"Invalid"<<std::endl; goto train2;}
    Currarmy = Currarmy + train * hitpoint;
    gold = gold - train * Tg;
    food = food - train * Tf;
    Currarmy = War(enemyarmy, Currarmy);
    if( Currarmy < 0 ){std::cout<<"You Have Been Defeated"<<std::endl; return 0;}
        
  }   

}