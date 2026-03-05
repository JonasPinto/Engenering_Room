#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>

typedef struct {
    uint8_t *buffer;
    size_t size;
    size_t offset;
} Arena;

/**
 * Initializes the arena by pre-allocating a fixed block of memory.
 */
Arena arena_init(size_t size) {
    return (Arena){
        .buffer = (uint8_t *)malloc(size),
        .size = size,
        .offset = 0
    };
}

/**
 * Allocates a memory block from the arena. 
 * Implements 8-byte alignment for performance and hardware compatibility.
 */
void *arena_alloc(Arena *a, size_t size) {
    // Memory alignment: aligns the size to the next multiple of 8.
    size_t aligned_size = (size + 7) & ~7;
    
    if (a->offset + aligned_size <= a->size) {
        void *ptr = &a->buffer[a->offset];
        a->offset += aligned_size;
        return ptr;
    }
    return NULL; 
}

/**
 * Resets the offset to zero. Effectively "frees" all memory in O(1).
 */
void arena_reset(Arena *a) {
    a->offset = 0;
}

/**
 * Releases the pre-allocated block back to the operating system.
 */
void arena_free(Arena *a) {
    free(a->buffer);
    a->buffer = NULL;
    a->size = 0;
    a->offset = 0;
}