function minimalNumberOfPackages(
    items,
    availableLargePackages,
    availableSmallPackages
) {
    // Your code goes here
    if (items > availableLargePackages * 5 + availableSmallPackages) {
        return -1;
    }

    const largePackages =
        Math.ceil(items / 5) > availableLargePackages
            ? availableLargePackages
            : Math.ceil(items / 5);
    if (largePackages * 5 >= items) {
        return largePackages;
    } else {
        return items - largePackages * 5 + largePackages;
    }
}

console.log(minimalNumberOfPackages(400, 30, 350));
console.log(minimalNumberOfPackages(400, 0, 400));
console.log(minimalNumberOfPackages(400, 30, 0));
console.log(minimalNumberOfPackages(400, 0, 399));
console.log(minimalNumberOfPackages(400, 80, 0));
