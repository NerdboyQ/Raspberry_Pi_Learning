#include <iostream>
#include <bitset>

using namespace std;

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

uint64_t clr_nth_bit(uint64_t val, uint16_t bit_pos){
	/**
	* Clears the bit in the provided value at the target bit position
	* using bitwise operators.
	*
	* @param val : address to manipulate.
	* @param bit_pos : bit position to clear.
	*/
	
	uint64_t adjust_bitset = ~(1 << bit_pos); // The << shifts a 1 to the left a number of bit positions, then NOT the bits.
	cout << "clr adjust_bitset: "  << bitset<16>(adjust_bitset) << endl; 
	val = val & adjust_bitset; // We AND the value provided with the adjust_bitset forcing it to a 0 value.
	return val;
}

uint16_t get_nth_bit(uint64_t val, uint16_t bit_pos){
	/**
	* Gets the bit in the provided value at the target bit position
	* using bitwise operators.
	*
	* @param val : address to manipulate.
	* @param bit_pos : bit position to grab.
	*/

	val = (val >> bit_pos); // We use the >> bitwise operator to shift the value to the right until the target bit is furthest to the right.
	cout << "get adjusted bitset: " << bitset<16>(val) << endl;
	uint16_t bit =  val & 1; // We then AND it with a 1 to get the target bit we shifted to the right in the previous step.
	return bit;
}

uint64_t set_nth_bit(uint64_t val, uint16_t bit_pos){
	/**
	* Sets the bit in the provided value at the target bit position
	* using bitwise operators.
	*
	* @param val : address to manipulate.
	* @param bit_pos : bit position to set.
	*/
	
	uint64_t adjust_bitset = (1 << bit_pos); // The << shifts a 1 to the left a number of bit positions.
	cout << "set adjust_bitset: "  << bitset<16>(adjust_bitset) << endl;
	val = val | adjust_bitset; // We OR the bit at a position with a 1 forcing it to a 1 value.
	return val;
}

uint64_t old_addr = 0xA5A5;

int main(){
	fibonacci_sequence(100);
	uint64_t set_addr = set_nth_bit(old_addr, 1);
	uint64_t clr_addr = clr_nth_bit(old_addr, 0);
	cout << "old: " << hex << old_addr <<  ", " << bitset<16>(old_addr) << endl; 
	cout << "set: " << hex << set_addr <<  ", " << bitset<16>(set_addr) << endl; 
	cout << "clr: " << hex << clr_addr <<  ", " << bitset<16>(clr_addr) << endl; 
	cout << get_nth_bit(old_addr, 5) << endl;
	return 0;
}