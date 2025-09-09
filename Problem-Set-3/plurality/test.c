#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAX 9

typedef struct
{
    string name;
    int vote;
} candidate;

// Global variables
candidate candidates[MAX];
int candidate_count;   // <<< GLOBAL now

bool vote(string name);

int main(void)
{
    candidate_count = 2;   // Set how many candidates you have

    candidates[0].name = "Tallal";
    candidates[0].vote = 1;
    candidates[1].name = "noone";
    candidates[1].vote = 0;

    string name = "k";
    if (!vote(name))
    {
        printf("Invalid vote.\n");
    }
    else
    {
        printf("%i\n", candidates[0].vote);
    }
}

bool vote(string name)
{
    int i = 0;
    while (i < candidate_count)    // now it works!
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].vote++;
            return true;
        }
        i++;
    }
    return false;
}
