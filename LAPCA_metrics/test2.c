#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
    int data;
    struct node *next;
}node;


node* createLinkedList(int n, int *arr){
    node *head = NULL, *iter = NULL, *newNode = NULL;
    
    node* dummyhead = (node*)malloc(sizeof(node));
    dummyhead->next = NULL;
    dummyhead->data = 0;
    head = dummyhead;
    iter = head;

    for(int i = 0; i < n; i++){
        newNode = (node*)malloc(sizeof(node));
        newNode->data = arr[i];
        newNode->next = NULL;
        iter->next = newNode;
        iter = iter->next;
    }

    return head->next;
}


void insert(node *head, int pos, int data){
	node* p = head;
	node* q = NULL;
	node *newnode = malloc(sizeof(node));
	newnode->data = data;
	newnode->next = NULL;
	if(head == NULL){
	head = newnode;
	}
	else{
	for(int i=0;i<pos;i++){
	q = p;
	p = p->next;
	}
	newnode->next = p;
	q->next = newnode;
	}
}


void delete(node *head){
	if(head == NULL){
	return;
	}
	node *prev = head;
	node *curr = prev->next;
	while(curr!=NULL && prev!=NULL){
	prev->next = curr->next;
	free(curr);
	prev = prev->next;
	if(prev!=NULL){
	curr = prev->next;
	}
	}
}


int countNodes(node *head){
	node* p = head;
	int count = 0;
	if(head==NULL){
		return 0;
	}
	else{
	while(p!=NULL){
	count++;
	p = p->next;
	}
	return count;
	}	
}


void printList(node *head){
    if(head == NULL){
        printf("List empty!\n");
    }
    node *iter = head;
    while(iter != NULL){
        printf("%d ", iter->data);
        iter = iter->next;
    }
    printf("\n");
}


int main(){

    int no_of_nodes;
    scanf("%d",&no_of_nodes);

    int *arr = (int *)malloc(no_of_nodes*sizeof(int));
    for(int i=0;i<no_of_nodes;i++){
        scanf("%d",&arr[i]);
    }   

    node *head = createLinkedList(no_of_nodes, arr);

    int testcases;
    scanf("%d",&testcases);
    int position, data;

    for(int i = 0; i < testcases; i++){
        int operation;
        scanf("%d",&operation);
        switch(operation){
            case 1:
                // Insert at the given position 
                scanf("%d %d", &position, &data);
                insert(head, position, data);
                break;
            case 2:
                // Delete alternate nodes, starting from the node at index position 1
                delete(head);
                break;
            case 3:
                // Count the number of nodes
                no_of_nodes = countNodes(head);
                printf("%d \n", no_of_nodes);
                break;
            case 4:
                // Print the list
                printList(head);
                break;
        }
    }
    return 0;
}
