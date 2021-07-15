#include <iostream>
#include <bitset>
#include <cstring>

using namespace std;

class BitManipulator
{
	public :
		uint32_t address;

		BitManipulator(uint32_t addr)
		{
			this -> address = addr;
			cout << "The user provided the following address: 0x" << hex << address << endl;
			cout << "The bit representation of the address is: " << bitset<16>(address) << endl;
			get_nth_bit(3);
			toggle_nth_bit(2);
			set_nth_bit(4);
			clear_nth_bit(3);
		}

		void get_nth_bit(uint16_t bit_position)
		{
			// Shifts the address to the right to make the target bit the first bit (bit 0)
			// then use the AND operator to mask all other bits with 0's, only returning bit 0
			uint16_t nth_bit = (address >> bit_position) & 0x1;
			cout << endl << "The bit found at bit position " << bit_position << " is: " << nth_bit << endl;
		}

		void set_nth_bit(uint16_t bit_position)
		{
			// Shifts a single bit, 1, to the target bit position to mask/ignore all other bit positions
			// then the OR operator is used to force the value to a 1.
			uint32_t new_address = (0x1 << bit_position) | address;
			cout << endl << "Setting bit at position: " << bit_position << endl;
			cout << "old: " << bitset<16>(address) << endl;
			cout << "new: " << bitset<16>(new_address) << endl;
		}

		void clear_nth_bit(uint16_t bit_position)
		{
			// Shifts a single bit, 1, to the left until the 1 is in the target bit position 
			// and use the NOT operator to get the inverse of all the bits e.g. 000100 -> 111011
			// then the AND operator is used with the inverse address and the address to force the
			// target bit position to a 0. 
			uint32_t new_address = ~(1 << bit_position) & address;
			cout << endl << "Clearing bit at position: " << bit_position << endl;
			cout << "old: " << bitset<16>(address) << endl;
			cout << "new: " << bitset<16>(new_address) << endl;
		}

		void toggle_nth_bit(uint16_t bit_position)
		{
			// Shifts a single bit 1 to the left until the 1 is in the target bit position
			// then the XOR operator is used with the single bit and the address to force the 
			// target bit position to flip to it's oposite value. 1->0 or 0->1
			uint32_t new_address = (0x1 << bit_position) ^ address;
			cout << "toggle 1" << endl;
			cout << "old: " << bitset<16>(address) << endl;
			cout << "new: " << bitset<16>(new_address) << endl;

			cout << "toggle 2" << endl;
			cout << "old: " << bitset<16>(new_address) << endl;
			new_address = (0x1 << bit_position) ^ new_address;
			cout << "new: " << bitset<16>(new_address) << endl;
		}

};

class LinkedListExample
{
	

	class SinglyLinkedList
	{
		// Singly Linked List
		class Node 
		{
		public:
			int data;
			Node *next;
		};
		
	public:

		SinglyLinkedList()
		{
			Node * head = NULL;
			Node * second = NULL;
			Node * third = NULL;

			head = new Node();
			second = new Node();
			third = new Node();

			head->data = 1;
			head->next = second;

			second->data = 2;
			second->next = third;

			third->data = 3;
			third->next = NULL;
			cout << "Head: " << head->data << ", Second: " << second->data << ", Third: " << third->data << endl;
		}
		

	};

	class DoublyLinkedList
	{

		// Doubly Linked List
		class Node 
		{
		public:
			int data;
			Node *previous;
			Node *next;
		};
	public:

		DoublyLinkedList()
		{
			Node * head = NULL;
			Node * second = NULL;
			Node * third = NULL;

			head = new Node();
			second = new Node();
			third = new Node();

			head->data = 1;
			head->next = second;
			head->previous = NULL;

			second->data = 2;
			second->next = third;
			second->previous = head;

			third->data = 3;
			third->next = NULL;
			third->previous = second;
			cout << "Head: " << head->data << ", Second: " << second->data << ", Third: " << third->data << endl;
		}

	};
public:
	LinkedListExample(){
		SinglyLinkedList();
		DoublyLinkedList();
	}
};



void fibonacci_sequence(uint16_t max){
	/**
	* Displays the Fibonacci sequence until the max value is reached.
	*
	* @param max : max value for the sequence
	*/
	int _old = 0;
	int _new = 0;
	int _hol = 0;

	cout << "Below is your desired Fibonacci Sequence: " << endl;
	while (_new < max){
		// cout << "old: " << _old << ", new: " << _new << endl;
		if (_new == 0) {
			cout << _new;
			_new ++;
		} else if (_new == 1 && _old == 0){
			cout << ", " << _new;
			_old ++;
		} else if(_new == 1 && _old == 1){
			cout << ", " << _new;
			_new++;
		} else {
			cout << ", " << _new;
			_hol = _old;
			_old = _new;
			_new += _hol;
		}
	}
	cout << endl << endl;
}

void pointer_example(){
	/**
	* Provides example of how to assign and de-reference a pointer.
	* A pointer points to a specific address in memory. 
	*
	*/

	uint16_t var = 50;
	uint16_t *p;
	p = &var;
	cout << "pointer address:\t\t\t" << p << endl;
	cout << "value of variable:\t\t\t" << dec << var << endl;
	cout << "value in pointer's address:\t" << dec << *p << endl;
}

void increment_operator_comparisons(){
	/** 
	* Illustrates the differences in ++value vs value++
	*
	*
	*/

	int a = 1;
	int b = 1;
	int j = ++a; // increments a and returns the incremented value to assign for j
	int k = b++; // increments b but returns the original b value to assign for k
	cout << "a: " << a << ", j: " << j << endl;
	cout << "b: " << b << ", k: " << k << endl;
}

int main(){
	cout << "==============================================================" << endl << endl;
	fibonacci_sequence(100);
	cout << "==============================================================" << endl << endl;
	increment_operator_comparisons();
	cout  << endl << "==============================================================" << endl << endl;
	BitManipulator bitManipulator = BitManipulator(0x1F2F3F4F);
	cout  << endl << "==============================================================" << endl << endl;
	LinkedListExample();
	return 0;
}