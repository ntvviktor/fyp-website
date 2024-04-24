function texts() {
    return {
        truncated: [false, false],
        truncatable: [false, false],
        texts: [
            "{{ book.description | safe }}"
        ],
        setTruncate(index, element) {
            if (element.offsetHeight < element.scrollHeight ||
                element.offsetWidth < element.scrollWidth) {
                // your element has an overflow
                // show read more button
                this.truncated[index] = true;
                this.truncatable[index] = true;
            } else {
                // your element doesn't have overflow
                this.truncated[index] = false;
                this.truncatable[index] = false;
            }
        },
        isTruncated(index) {
            return true;
        }
    }
}